from django.contrib.auth.models import User
from django.db import models


class Avatar(models.Model):
    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"
    
    src = models.ImageField(upload_to="media/users/avatars/", verbose_name="url")
    alt = models.CharField(max_length=100, blank=True, verbose_name="description")


class Profile(models.Model):
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="user")
    fullname = models.CharField(max_length=100, blank=True, verbose_name="full name")
    phone = models.CharField(max_length=100, blank=True, unique=True, verbose_name="phone number")
    avatar = models.OneToOneField(Avatar, blank=True, on_delete=models.CASCADE, related_name="profile", verbose_name="avatar")

