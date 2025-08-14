from django.db import models
from apps.library.validators import (
    validate_isbn,
    validate_published_date,
    validate_pages,
)


class Book(models.Model):
    # Model to book management

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=10, unique=True)
    pages = models.PositiveIntegerField()

    def clean(self):
        validate_isbn(self.isbn)
        validate_published_date(self.published_date)
        validate_pages(self.pages)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["isbn"],
                name="unique_isbn",
                violation_error_message="El ISBN debe ser único. Ya existe un libro con este ISBN.",
            ),
        ]

    def __str__(self):
        return self.title
