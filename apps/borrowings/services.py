from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from apps.books.models import Book
from .models import Borrowing
from apps.members.models import Member


@transaction.atomic
def borrow_book(*, book, member):

    """
    Services for borrowing book.
    """

    if member.status != Member.MembershipStatus.ACTIVE:
        raise ValidationError("Your membership is suspended.")

    book = Book.objects.select_for_update().get(pk=book.pk)

    if not member.can_borrow_more:    
        raise ValidationError(
            "Cannot borrow: limit reached, overdue books, or unpaid fines."
        )

    if book.available_copies < 1:
        raise ValidationError("No available copies of this book.")

    borrowing = Borrowing.objects.create(
        book=book,
        member=member,
        due_date=timezone.now().date() + timedelta(days=Borrowing.BORROW_PERIOD_DAYS),
    )

    book.available_copies -= 1
    book.save(update_fields=["available_copies"])

    return borrowing


@transaction.atomic
def return_book(*, borrowing, member):

    """
    Services for returning the book.
    """

    if borrowing.member != member:
        raise ValidationError("You cannot return this book.")

    if borrowing.status == Borrowing.BorrowStatus.RETURNED:
        raise ValidationError("This book has already been returned.")

    borrowing.returned_date = timezone.now().date()
    borrowing.fine_amount = borrowing.days_overdue * Borrowing.FINE_PER_DAY
    borrowing.status = Borrowing.BorrowStatus.RETURNED
    borrowing.save()

    book = borrowing.book
    book.available_copies += 1
    book.save(update_fields=["available_copies"])

    return borrowing


@transaction.atomic
def pay_fine(*, borrowing, member):

    """
    Services for paying fine.
    """

    if borrowing.member != member:
        raise ValidationError("You cannot pay this fine.")

    if borrowing.fine_amount <= 0:
        raise ValidationError("There is no fine to pay.")
    
    if borrowing.fine_paid:
        raise ValidationError("This fine has already been paid.")

    borrowing.fine_paid = True
    borrowing.fine_paid_date = timezone.now().date()
    borrowing.save()

    return borrowing