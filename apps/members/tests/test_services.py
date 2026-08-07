import pytest

from apps.members.models import Member
from apps.members.services import (
    create_member,
    suspend_member,
    reactivate_member,
)
from apps.users.models import User
from apps.members.factories import MemberFactory

@pytest.mark.django_db
def test_create_member_creates_user_and_member():

    member = create_member(
        first_name="Manoj",
        last_name="Pun",
        email="manoj@example.com",
        password="password123",
        phone_number="9800000000",
        address="Kathmandu",
    )

    assert member.user.first_name == "Manoj"
    assert member.user.last_name == "Pun"
    assert member.user.email == "manoj@example.com"
    assert member.phone_number == "9800000000"
    assert member.membership_number == "MEM-00001"
    assert member.user.role == User.Role.MEMBER


@pytest.mark.django_db
def test_membership_number_increments():

    first = create_member(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="password123",
        phone_number="9800000001",
    )

    second = create_member(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        password="password123",
        phone_number="9800000002",
    )

    assert first.membership_number == "MEM-00001"
    assert second.membership_number == "MEM-00002"


@pytest.mark.django_db
def test_suspend_member():

    member = MemberFactory()

    suspend_member(member=member)

    member.refresh_from_db()

    assert member.status == Member.MembershipStatus.SUSPENDED


@pytest.mark.django_db
def test_reactivate_member():

    member = MemberFactory(
        status=Member.MembershipStatus.SUSPENDED,
    )

    reactivate_member(member=member)

    member.refresh_from_db()

    assert member.status == Member.MembershipStatus.ACTIVE