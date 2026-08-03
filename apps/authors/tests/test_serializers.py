from apps.authors.serializers import AuthorCreateUpdateSerializer
from datetime import date, timedelta

def test_first_name_must_be_title():
    serializer = AuthorCreateUpdateSerializer(
        data = {
            "first_name" : "Manoj",
            "last_name" : "Pun"
        }
    )

    assert serializer.is_valid()
    assert serializer.validated_data["first_name"] == "Manoj"


def test_first_name_cannot_be_blank():
    serializer = AuthorCreateUpdateSerializer(
        data={
            "first_name": "   ",
            "last_name": "Orwell"
        }
    )

    assert not serializer.is_valid()
    assert "first_name" in serializer.errors


def test_last_name_can_be_empty():
    serializer = AuthorCreateUpdateSerializer(
        data={
            "first_name": "George",
            "last_name": ""
        }
    )

    assert serializer.is_valid()
    assert serializer.validated_data["last_name"] == ""


def test_birth_date_cannot_be_future():

    serializer = AuthorCreateUpdateSerializer(
        data={
            "first_name": "George",
            "birth_date": date.today() + timedelta(days=10)
        }
    )

    assert not serializer.is_valid()
    assert "birth_date" in serializer.errors