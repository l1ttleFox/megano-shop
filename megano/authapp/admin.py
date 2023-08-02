from django.contrib import admin
from authapp import models


@admin.register(models.Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ("alt",)
    fields = ["alt", "src"]
    list_filter = ("id", "alt")
    

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "phone")
    fields = ["id", "user", "fullname", "phone", "avatar"]
    list_filter = ("id", "fullname")
    