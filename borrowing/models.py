from django.db import models
from django.db.models import Q

from book.models import Book
from library_service import settings


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(expected_return_date__gte=models.F("borrow_date")),
                name="expected_return_date_gte_borrow_date",
            ),
            models.CheckConstraint(
                condition=(
                    Q(actual_return_date__isnull=True)
                    | Q(actual_return_date__gte=models.F("borrow_date"))
                ),
                name="actual_return_date_gte_borrow_date",
            ),
        ]
