import pytest

from apps.members.factories import MemberFactory
from apps.users.factories import UserFactory
from apps.members.serializers import MemberCreateSerializer, MemberUpdateSerializer

@pytest.mark.django_db
def test_create_member_serializer_creates_member():

    serializer = MemberCreateSerializer(
        data={
            "email": "manoj@example.com",
            "password": "password123",
            "first_name": "Manoj",
            "last_name": "Pun",
            "phone_number": "9800000000",
            "address": "Kathmandu",
        }
    )

    assert serializer.is_valid()

    member = serializer.save()

    assert member.user.email == "manoj@example.com"
    assert member.user.first_name == "Manoj"
    assert member.membership_number == "MEM-00001"


@pytest.mark.django_db
def test_first_name_cannot_be_blank():

    serializer = MemberCreateSerializer(
        data={
            "email": "manoj@example.com",
            "password": "password123",
            "first_name": "   ",
            "last_name": "Pun",
            "phone_number": "9800000000",
            "address": "Kathmandu",
        }
    )

    assert not serializer.is_valid()

    assert serializer.errors["first_name"] == [
        "First name cannot be blank."
    ]


@pytest.mark.django_db
def test_email_must_be_unique():

    UserFactory(email="manoj@example.com")

    serializer = MemberCreateSerializer(
        data={
            "email": "manoj@example.com",
            "password": "password123",
            "first_name": "Manoj",
            "last_name": "Pun",
            "phone_number": "9800000000",
            "address": "Kathmandu",
        }
    )

    assert not serializer.is_valid()

    assert serializer.errors["email"] == [
        "A user with this email already exists."
    ]


@pytest.mark.django_db
def test_update_serializer_updates_member_and_user():

    member = MemberFactory(
        phone_number="9800000000",
        address="Old Address",
    )

    serializer = MemberUpdateSerializer(
        instance=member,
        data={
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "9811111111",
            "address": "New Address",
        },
    )

    assert serializer.is_valid(), serializer.errors

    updated_member = serializer.save()

    updated_member.user.refresh_from_db()
    updated_member.refresh_from_db()

    assert updated_member.user.first_name == "John"
    assert updated_member.user.last_name == "Doe"
    assert updated_member.phone_number == "9811111111"
    assert updated_member.address == "New Address"


@pytest.mark.django_db
def test_update_serializer_can_partially_update_member():

    member = MemberFactory(
        phone_number="9800000000",
    )

    original_first_name = member.user.first_name

    serializer = MemberUpdateSerializer(
        instance=member,
        data={
            "phone_number": "9811111111",
        },
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors

    updated_member = serializer.save()

    assert updated_member.phone_number == "9811111111"
    assert updated_member.user.first_name == original_first_name