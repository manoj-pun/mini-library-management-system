from rest_framework.viewsets import ModelViewSet
from .models import Book
from apps.common.permissions import IsLibrarian, IsMember
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    BookListSerializer,
    BookCreateUpdateSerializer,
    BookDetailSerializer
)

class BookViewSet(ModelViewSet):

    """
    Viewset for managing books.
    Members can only list the books.
    """

    queryset = Book.objects.prefetch_related("authors")
    search_fields = ["title", "genre"]
    ordering_fields = ["title", "created_at"]

    def get_permissions(self):
        if self.action in ["create", "retrieve", "update", "partial_update", "destroy"]:
            return [IsLibrarian()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return BookCreateUpdateSerializer
        return BookDetailSerializer
