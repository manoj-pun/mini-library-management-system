from django.db import models
import uuid
from django.conf import settings

class Member(models.Model):
    class MembershipStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="member")
    membership_number = models.CharField(max_length=20, editable=False, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=MembershipStatus.choices, default=MembershipStatus.ACTIVE)
    max_books_allowed = models.PositiveIntegerField(default=3)
    joined_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        full_name = self.user.get_full_name() or self.user.email
        return f"{self.membership_number} - {full_name}"

    class Meta:
        db_table = "members"
        ordering = ["-joined_date"]

    @property
    def active_borrow_count(self):
        return self.borrow_records.filter(status="BORROWED").count()

    @property
    def has_overdue_books(self):
        return any(
            record.is_overdue for record in self.borrow_records.filter(status="BORROWED")
        )

    @property
    def has_unpaid_fines(self):
        return self.borrow_records.filter(fine_amount__gt=0, fine_paid=False).exists()

    @property
    def can_borrow_more(self):
        return (
            self.status == self.MembershipStatus.ACTIVE
            and self.active_borrow_count < self.max_books_allowed
            and not self.has_overdue_books
            and not self.has_unpaid_fines
        )




