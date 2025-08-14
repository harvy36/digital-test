from django.core.exceptions import ValidationError
from datetime import date


def validate_isbn(value):
    if len(value) != 10:
        raise ValidationError("El ISBN debe tener 10 digitos.")


def validate_published_date(value):
    if value > date.today():
        raise ValidationError("La fecha de publicación no puede ser futura.")


def validate_pages(value):
    if value <= 0:
        raise ValidationError("El número de páginas debe ser positivo.")
