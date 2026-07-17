from rest_framework.viewsets import ModelViewSet
from .models import Author
from .serializers import (
    AuthorCreateUpdateSerializer,
    AuthorDetailSerializer,
    AuthorListSerializer
)

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name","birth_date","created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        if self.action in ["create","update","partial_update"]:
            return AuthorCreateUpdateSerializer
        return AuthorDetailSerializer