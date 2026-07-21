from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.common.permissions import IsLibrarian, IsMember
from .models import Member
from .serializers import (
    MemberCreateSerializer,
    MemberUpdateSerializer,
    MemberListSerializer,
    MemberDetailSerializer
)

class MemberViewSet(ModelViewSet):

    """
    ViewSet for managing library members.

    Librarians can create, retrieve, update, and delete members.
    Authenticated members can access their own profile through the
    `me` action.
    """

    queryset = Member.objects.select_related("user")
    permission_classes = [IsLibrarian]
    search_fields = ["user__first_name", "user__last_name", "membership_number"]
    ordering_fields = ["joined_date", "membership_number"]

    def get_serializer_class(self):
        if self.action == "list":
            return MemberListSerializer
        if self.action == "create":
            return MemberCreateSerializer
        if self.action in ["update", "partial_update"]:
            return MemberUpdateSerializer
        return MemberDetailSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        return Response(MemberDetailSerializer(member).data,status=status.HTTP_201_CREATED)
    
    @action(detail=False,methods=["get"],permission_classes=[IsMember])
    def me(self, request):
        serializer = self.get_serializer(request.user.member)
        return Response(serializer.data)