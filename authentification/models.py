from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.username  # passe de <User object (1)> à username


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Suppresion si suppression parent
        related_name="following",  # = user.following.all()
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",  # = user.followers.all()
    )

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )  # SQL UNIQUE (user_id, followed_user_id)

    def clean(self):
        if self.user == self.followed_user:
            raise ValidationError("You cannot follow yourself.")
