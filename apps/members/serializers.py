from rest_framework import serializers
from .models import Member
from .services import create_member
from apps.users.models import User

class MemberCreateSerializer(serializers.ModelSerializer):

    """
    Serializer class for creating member.
    """

    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Member
        fields = ["email", "password", "first_name", "last_name", "phone_number", "address"]

    def validate_first_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "First name cannot be blank."
            )
        return value.title()
    
    def validate_last_name(self, value):
        return value.strip().title()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def create(self, validated_data):
        return create_member(**validated_data)


class MemberUpdateSerializer(serializers.ModelSerializer):

    """
    Serializer for updating member.
    Handles fields stored in both Member and related User models.
    """

    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30,required=False,allow_blank=True)

    class Meta:
        model = Member
        fields = ["first_name", "last_name", "phone_number", "address"]

    def update(self, instance, validated_data):
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)

        user = instance.user

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        user.save()
        return super().update(instance, validated_data)


class MemberListSerializer(serializers.ModelSerializer):

    """
    Serializer class for listing members.
    """

    first_name = serializers.CharField(source="user.first_name")

    class Meta:
        model = Member
        fields = ["id", "first_name", "membership_number", "phone_number"]


class MemberDetailSerializer(serializers.ModelSerializer):

    """
    Serializer class for retrieving member details.
    """

    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name") 

    class Meta:
        model = Member
        fields = ["id", "first_name", "last_name", "email", "membership_number", "phone_number", "address", "status", "joined_date"]


