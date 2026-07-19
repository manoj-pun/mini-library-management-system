from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
import uuid

class User(AbstractUser):
    class Role(models.TextChoices):
        LIBRARIAN = "LIBRARIAN", "Librarian"
        MEMBER = "MEMBER", "Member"

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)

    def __str__(self):
        return self.get_full_name() or self.email
    
    class Meta:
        db_table = "users"
        ordering = ["first_name","last_name"]
            