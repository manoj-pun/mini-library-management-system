from django.db import models
import uuid
from datetime import timezone

class Borrowing(models.Model):
    class BorrowStatus(models.TextChoices):
        BORROWED = "BORROWED", "Borrowed"
        RETURNED = "RETURNED", "Returned"

    FINE_PER_DAY = 5
    BORROW_PERIOD_DAYS = 20

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey("books.Book", on_delete=models.PROTECT, related_name="borrow_books")
    member = models.ForeignKey("members.Member", on_delete=models.PROTECT, related_name="borrow_books")
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=BorrowStatus.choices, default=BorrowStatus.BORROWED)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fine_paid = models.BooleanField(default=False)
    fine_paid_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "borrow_books"
        ordering = ["-borrowed_date"]

    def __str__(self):
        return f"{self.member} - {self.book.title}"
    
    @property
    def is_overdue(self):
        if self.status == self.BorrowStatus.RETURNED:
            return False
        return timezone.now().date() > self.due_date
    
    @property
    def days_overdue(self):
        reference_date = self.returned_date or timezone.now().date()
        return max((reference_date - self.due_date).days, 0)