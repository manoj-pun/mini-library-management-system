import pytest

from apps.members.factories import MemberFactory
from apps.members.models import Member

@pytest.mark.django_db
def test_librarian_can_create_member(api_client, librarian):
    api_client.force_authenticate(user=librarian)

    response = api_client.post(
        "/api/members/",
        {
            "email": "manoj@example.com",
            "password": "password123",
            "first_name": "Manoj",
            "last_name": "Pun",
            "phone_number": "9800000000",
            "address": "Kathmandu",
        },
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_member_cannot_create_member(api_client, member_user):
    api_client.force_authenticate(user=member_user)
    response = api_client.post(
        "/api/members/",
        {
            "email": "new@example.com",
            "password": "password123",
            "first_name": "John",
            "phone_number": "9800000000",
        },
        format="json"
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_librarian_can_update_member(api_client, librarian):

    member = MemberFactory()

    api_client.force_authenticate(user=librarian)

    response = api_client.put(
        f"/api/members/{member.id}/",
        {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "9811111111",
            "address": "Pokhara",
        },
        format="json",
    )

    assert response.status_code == 200

    member.refresh_from_db()
    member.user.refresh_from_db()

    assert member.user.first_name == "John"
    assert member.user.last_name == "Doe"
    assert member.phone_number == "9811111111"
    assert member.address == "Pokhara"


@pytest.mark.django_db
def test_librarian_can_suspend_member(api_client, librarian):

    member = MemberFactory()

    api_client.force_authenticate(user=librarian)

    response = api_client.post(
        f"/api/members/{member.id}/suspend/"
    )

    member.refresh_from_db()

    assert response.status_code == 200
    assert member.status == Member.MembershipStatus.SUSPENDED


@pytest.mark.django_db
def test_librarian_can_reactivate_member(api_client, librarian):

    member = MemberFactory(
        status=Member.MembershipStatus.SUSPENDED
    )

    api_client.force_authenticate(user=librarian)

    response = api_client.post(
        f"/api/members/{member.id}/reactivate/"
    )

    member.refresh_from_db()

    assert response.status_code == 200
    assert member.status == Member.MembershipStatus.ACTIVE


@pytest.mark.django_db
def test_member_can_view_own_profile(api_client, member_user):

    api_client.force_authenticate(user=member_user)

    response = api_client.get(
        "/api/members/me/"
    )

    assert response.status_code == 200
    assert response.data["email"] == member_user.email


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_members(api_client):

    response = api_client.get(
        "/api/members/"
    )

    assert response.status_code == 401
