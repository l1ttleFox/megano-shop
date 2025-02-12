from django.contrib.auth.models import User
from django.db import models


class Avatar(models.Model):
    """Модель аватара пользователя."""

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"
        ordering = ["id"]

    src = models.ImageField(
        upload_to="media/users/avatars/",
        default="authapp/static/images/base_avatar.jpg",
        verbose_name="url",
    )
    alt = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Avatar is not required",
        verbose_name="description",
    )

    @property
    def auto_alt(self):
        """Геттер описания аватара."""
        if self.alt:
            return self.alt
        return f"{self.profile.user.username}'s avatar"


class Profile(models.Model):
    """Модель профиля пользователя."""

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["id"]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name="user"
    )
    fullname = models.CharField(max_length=100, blank=True, verbose_name="full name")
    phone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=None,
        verbose_name="phone number",
    )
    avatar = models.OneToOneField(
        Avatar,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="avatar",
    )
