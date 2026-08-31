from django.db import models
from django.contrib.auth.models import User


class PhotoUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile_photo",
    )

    image = models.ImageField(
        upload_to="users/profile/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Photo - {self.user.username}"