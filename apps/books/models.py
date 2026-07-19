from django.db import models
import uuid

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("authors.Author",related_name="books")
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100, blank=True)
    published_date = models.DateField(null=True,blank=True)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "books"
        ordering = ["title"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(available_copies__lte=models.F("total_copies")),
                name="available_copies_lte_total_copies"
            )
        ]