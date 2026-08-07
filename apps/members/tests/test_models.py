import pytest
from datetime import timedelta
from django.utils import timezone

from apps.members.factories import MemberFactory
from apps.members.models import Member
from apps.borrowings.factories import BorrowingFactory
from apps.borrowings.models import Borrowing


@pytest.mark.django_db
def test_member_str_returns_membership_number_and_name():
    member = MemberFactory(
        membership_number="MEM-00001",
        user__first_name="John",
        user__last_name="Doe",
    )

    assert str(member) == "MEM-00001 - John Doe"


@pytest.mark.django_db
def test_member_str_user_email_when_name_is_blank():
    member = MemberFactory(
        user__first_name = "",
        user__last_name = "",
        user__email = "test@example.com",
        membership_number = "MEM-00001"
    )

    assert str(member) == "MEM-00001 - test@example.com"


@pytest.mark.django_db
def test_new_member_can_borrow_book():
    member = MemberFactory()

    assert member.can_borrow_more is True


@pytest.mark.django_db
def test_suspend_users_cannot_borrow_book():
    member = MemberFactory(
        status = Member.MembershipStatus.SUSPENDED
    )

    assert member.can_borrow_more is False


# @pytest.mark.django_db
# def test_book_borrow_count_counts_only_borrowed_books():

#     member = MemberFactory()

#     BorrowingFactory(
#         member=member,
#         status=Borrowing.BorrowStatus.BORROWED,
#     )

#     BorrowingFactory(
#         member=member,
#         status=Borrowing.BorrowStatus.BORROWED,
#     )

#     BorrowingFactory(
#         member=member,
#         status=Borrowing.BorrowStatus.BORROWED,
#     )

#     BorrowingFactory(
#         member=member,
#         status=Borrowing.BorrowStatus.RETURNED,
#     )

#     assert member.book_borrow_count == 3


@pytest.mark.django_db
def test_book_borrow_count_counts_only_borrowed_books():

    member = MemberFactory()

    BorrowingFactory.create_batch(
        3,
        member=member,
        status=Borrowing.BorrowStatus.BORROWED,
    )

    BorrowingFactory(
        member=member,
        status=Borrowing.BorrowStatus.RETURNED,
    )

    assert member.book_borrow_count == 3


@pytest.mark.django_db
def test_member_has_overdue_books():

    member = MemberFactory()

    BorrowingFactory(
        member=member,
        status=Borrowing.BorrowStatus.BORROWED,
        due_date=timezone.now().date() - timedelta(days=2),
    )

    assert member.has_overdue_books is True


@pytest.mark.django_db
def test_member_has_no_overdue_books():

    member = MemberFactory()

    BorrowingFactory(
        member=member,
        status=Borrowing.BorrowStatus.BORROWED,
        due_date=timezone.now().date() + timedelta(days=5),
    )

    assert member.has_overdue_books is False


@pytest.mark.django_db
def test_member_has_unpaid_fines():

    member = MemberFactory()

    BorrowingFactory(
        member=member,
        fine_amount=20,
        fine_paid=False,
    )

    assert member.has_unpaid_fines is True


@pytest.mark.django_db
def test_member_has_no_unpaid_fines():

    member = MemberFactory()

    BorrowingFactory(
        member=member,
        fine_amount=20,
        fine_paid=True,
    )

    assert member.has_unpaid_fines is False


@pytest.mark.django_db
def test_member_cannot_borrow_when_limit_reached():

    member = MemberFactory(max_books_allowed=3)

    BorrowingFactory.create_batch(
        3,
        member=member,
        status=Borrowing.BorrowStatus.BORROWED,
    )

    assert member.can_borrow_more is False

