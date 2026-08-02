import pytest
from apps.users.models import User


@pytest.mark.django_db
def test_create_user():

    User.objects.create_user(
        email="test@example.com",
        password="password123"
    )

    assert User.objects.count() == 1


@pytest.mark.django_db
def test_create_user_without_email():
    with pytest.raises(ValueError, match="Email is required."):
        User.objects.create_user(
            email="",
            password="password123",
        )

@pytest.mark.django_db
def test_email_normalization():

    user = User.objects.create_user(
        email="Test@Example.COM",
        password="password"
    )

    assert user.email == "Test@example.com"

@pytest.mark.django_db
def test_create_superuser():

    user = User.objects.create_superuser(
        email="admin@example.com",
        password="password123"
    )

    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.role == User.Role.LIBRARIAN