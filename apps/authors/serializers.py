from datetime import date
from rest_framework import serializers
from .models import Author

class AuthorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "birth_date"]

    def validate_first_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("First name cannot be empty")
        return value.title()
    
    def validate_last_name(self, value):
        value = value.strip()
        if not value:
            return ""
        return value.title()
    
    def validate_birth_date(self, value):
        if value and value > date.today():
            raise serializers.ValidationError("Birth date cannot be in the future")
        return value


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "birth_date"]


class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "birth_date", "created_at", "updated_at"]