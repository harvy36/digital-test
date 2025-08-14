from django.db import models
from apps.library.models import Book
from apps.users.validators import validate_loan
from django.contrib.auth import get_user_model

User = get_user_model()


class Member(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="member_profile"
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10, choices=[("staff", "Staff"), ("basic", "Basic")]
    )

    def __str__(self):
        return self.name


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Préstamo de {self.book} a {self.member}"

    def clean(self):
        validate_loan(self)
