from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


RATING_CHOICES = [
    (0, "0"),
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
]

class Review(models.Model):
    ticket = models.ForeignKey("tickets.Ticket", on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES,default=0,validators=[MinValueValidator(0),MaxValueValidator(5),]
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "ticket")  # blocage backend
