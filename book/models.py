from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["first_name", "last_name"]


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD", "HARD"
        SOFT = "SOFT", "SOFT"

    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover = models.CharField(
        max_length=4,
        choices=CoverChoices.choices,
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
