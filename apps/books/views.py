from rest_framework.viewsets import ModelViewSet
from .models import Book
from apps.common.permissions import IsLibrarian
from .serializers import (
    BookListSerializer,
    BookCreateUpdateSerializer,
    BookDetailSerializer
)

class BookViewSet(ModelViewSet):

    """
    Viewset for managing books.
    """

    queryset = Book.objects.all()
    permission_classes = [IsLibrarian]
    search_fields = ["title", "genre"]
    ordering_fields = ["title", "created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return BookCreateUpdateSerializer
        return BookDetailSerializer
