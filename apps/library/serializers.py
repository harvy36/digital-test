from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.library.models import Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate_isbn(self, value):
        if len(value) != 10:
            raise ValidationError("El ISBN debe tener 10 digitos.")
        return value

    def validate_unique_isbn(self, value):
        if Book.objects.filter(isbn=value).exists():
            raise ValidationError(
                "El ISBN debe ser único. Ya existe un libro con este ISBN."
            )
        return value

    def validate_published_date(self, value):
        if value > date.today():
            raise ValidationError("La fecha de publicación no puede ser futura.")
        return value

    def validate_pages(self, value):
        if value <= 0:
            raise ValidationError("El número de páginas debe ser positivo.")
        return value
