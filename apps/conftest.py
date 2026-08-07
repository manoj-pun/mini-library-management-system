import pytest
from rest_framework.test import APIClient
from apps.users.factories import UserFactory
from apps.members.factories import MemberFactory
from apps.users.models import User

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def member():
    return MemberFactory()


@pytest.fixture
def member_user(member):
    return member.user


@pytest.fixture
def librarian():
    return UserFactory(role=User.Role.LIBRARIAN)