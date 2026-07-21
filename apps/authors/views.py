from rest_framework.viewsets import ModelViewSet
from .models import Author
from .serializers import (
    AuthorCreateUpdateSerializer,
    AuthorDetailSerializer,
    AuthorListSerializer
)
from apps.common.permissions import IsLibrarian

class AuthorViewSet(ModelViewSet):

    """
    Viewset for managing authors.
    """

    queryset = Author.objects.prefetch_related("books")
    permission_classes = [IsLibrarian]
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name","birth_date","created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        if self.action in ["create","update","partial_update"]:
            return AuthorCreateUpdateSerializer
        return AuthorDetailSerializer