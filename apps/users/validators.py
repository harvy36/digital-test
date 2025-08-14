from django.core.exceptions import ValidationError


def validate_loan(loan):
    from apps.users.models import Loan

    if loan.end_date < loan.start_date:
        raise ValidationError(
            "La fecha de fin no puede ser anterior a la fecha de inicio."
        )

    if Loan.objects.filter(book=loan.book, returned_at__isnull=True).exists():
        raise ValidationError("El libro ya tiene un préstamo activo.")

    if loan.returned_at is not None and loan.returned_at < loan.start_date:
        raise ValidationError(
            "La fecha de devolución no puede ser anterior a la fecha de inicio."
        )
