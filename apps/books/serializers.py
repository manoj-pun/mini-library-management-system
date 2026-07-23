from rest_framework import serializers
from .models import Book
from apps.authors.models import Author

class AuthorNestedSerializer(serializers.ModelSerializer):

    """
    Serializer class to show the authors.
    """

    class Meta:
        model = Author
        fields = ["first_name", "last_name"]


class BookCreateUpdateSerializer(serializers.ModelSerializer):

    """
    Serializer class to create and update books.
    """

    class Meta:
        model = Book
        fields = ["title", "authors", "isbn", "genre", "published_date", "total_copies"]

    def create(self, validated_data):
        validated_data["available_copies"] = validated_data["total_copies"]
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if "total_copies" in validated_data:
            difference = (validated_data["total_copies"] - instance.total_copies)

            instance.available_copies += difference

        return super().update(instance, validated_data)


class BookListSerializer(serializers.ModelSerializer):

    """
    Serializer class for listing books.
    """
    authors = AuthorNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "isbn", "authors", "available_copies"]


class BookDetailSerializer(serializers.ModelSerializer):

    """
    Serializer class for retrieving book details.
    """

    authors = AuthorNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "isbn", "authors", "genre", "published_date", "total_copies", "available_copies", "created_at"]