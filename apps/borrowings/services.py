# apps/borrowing/services.py

from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.books.models import Book
from .models import BorrowRecord, BorrowStatus


@transaction.atomic
def borrow_book(*, book_id, member):
    book = Book.objects.select_for_update().get(pk=book_id)

    if not member.can_borrow_more:          # ← THIS is where can_borrow_more gets used
        raise ValidationError(
            "Cannot borrow: limit reached, overdue books, or unpaid fines."
        )

    if book.available_copies < 1:
        raise ValidationError("No available copies of this book.")

    borrow_record = BorrowRecord.objects.create(
        book=book,
        member=member,
        due_date=timezone.now().date() + timedelta(days=BorrowRecord.BORROW_PERIOD_DAYS),
        status=BorrowStatus.BORROWED,
    )

    book.available_copies -= 1
    book.save()

    return borrow_record