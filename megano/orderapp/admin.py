from django.contrib import admin
from orderapp import models


@admin.register(models.Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("id", "order_products", "order")
    fields = ["id", "order_products", "order"]


@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("id", "count", "product")
    fields = ["id", "count", "product", "basket"]
    list_filter = ("id", "count")
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ("id", "createdAt", "last_edited", "status", "deliveryType")
    fieldsets = [
        ("Base info", {
            "fields": ("id", "basket", "status", "user", "createdAt", "last_edited"),
        }),
        ("Delivery", {
            "fields": ("city", "address", "deliveryType"),
            "classes": ("wide",),
        }),
        ("payment", {
            "fields": ("payment", "paymentType"),
        })
    ]


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("number", "month", "year", "code")
    fields = ["name", "number", "month", "year", "code", "order"]
    
