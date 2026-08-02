import pytest
from apps.users.models import User


@pytest.mark.django_db
def test_user_has_uuid():

    user = User.objects.create_user(
        email="john@example.com",
        password="password"
    )

    assert user.id is not None


@pytest.mark.django_db
def test_default_role():

    user = User.objects.create_user(
        email="john@example.com",
        password="password"
    )

    assert user.role == User.Role.MEMBER


@pytest.mark.django_db
def test_user_str():

    user = User.objects.create_user(
        email="john@example.com",
        password="password",
        first_name="John",
        last_name="Smith"
    )

    assert str(user) == "John Smith"