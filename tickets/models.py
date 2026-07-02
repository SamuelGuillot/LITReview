from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tickets/", blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
