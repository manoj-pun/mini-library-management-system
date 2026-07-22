from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Borrowing
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    BorrowCreateSerializer,
    BorrowListSerializer,
    BorrowDetailSerializer
)
from .services import (
    borrow_book,
    return_book,
    pay_fine
)

class BorrowingViewSet(ReadOnlyModelViewSet):

    """
    ViewSet for managing borrowing records.
    """

    queryset = Borrowing.objects.select_related("book", "member")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == self.request.user.Role.LIBRARIAN:
            return queryset
        return queryset.filter(member=self.request.user.member)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowListSerializer
        if self.action == "borrow":
            return BorrowCreateSerializer
        return BorrowDetailSerializer

    @action(detail=False, methods=["post"])
    def borrow(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrowing = borrow_book(
            book = serializer.validated_data["book"],
            member = self.request.user.member
        )
        return Response(BorrowDetailSerializer(borrowing).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="return")
    def return_action(self, request, pk=None):
        borrowing = self.get_object()
        borrowing = return_book(
            borrowing = borrowing,
            member = self.request.user.member
        )
        return Response(BorrowDetailSerializer(borrowing).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="pay-fine")
    def pay_fine_action(self, request, pk=None):
        borrowing = self.get_object()
        borrowing = pay_fine(
            borrowing=borrowing,
            member=self.request.user.member
        )
        return Response(BorrowDetailSerializer(borrowing).data, status=status.HTTP_200_OK)
