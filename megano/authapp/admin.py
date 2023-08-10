from django.contrib import admin
from authapp import models


class ProfileInline(admin.TabularInline):
    model = models.Profile


@admin.register(models.Avatar)
class AvatarAdmin(admin.ModelAdmin):
    """Регистрация модели аватара в админке."""
    
    list_display = ("alt", "src")
    fields = ["alt", "src"]
    list_filter = ("id", "alt")
    inlines = [
        ProfileInline,
    ]
    

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Регистрация модели профиля пользователя в админке."""
    
    list_display = ("id", "fullname", "phone")
    fields = ["id", "user", "fullname", "phone", "avatar"]
    list_filter = ("id", "fullname")
    