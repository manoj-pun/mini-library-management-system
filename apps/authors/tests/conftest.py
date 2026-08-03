import pytest
from apps.users.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def librarian_user():
    return User.objects.create_user(
        email="librarian@test.com",
        role="LIBRARIAN",
        password="password123"
    )


@pytest.fixture
def member_user():
    return User.objects.create_user(
        email="member@test.com",
        role="MEMBER",
        password="password123"
    )