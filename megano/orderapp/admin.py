from django.contrib import admin
from orderapp import models


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    

class OrderInline(admin.TabularInline):
    model = models.Order
    
    
class PaymentInline(admin.TabularInline):
    model = models.Payment
    

@admin.register(models.Basket)
class BasketAdmin(admin.ModelAdmin):
    """Регистрация модели корзины в админке."""
    
    list_display = ("id", )
    inlines = [
        OrderProductInline,
        OrderInline,
    ]


@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    """Регистрация модели продукта в корзине в админке."""
    
    list_display = ("id", "count", "product")
    fields = ["count", "product", "basket"]
    list_filter = ("count", )
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """Регистрация модели заказа в админке."""
    
    list_filter = ("id", "createdAt", "last_edited", "status", "deliveryType")
    fieldsets = [
        ("Base info", {
            "fields": ("basket", "status", "user"),
        }),
        ("Delivery", {
            "fields": ("city", "address", "deliveryType"),
            "classes": ("wide",),
        }),
        ("payment", {
            "fields": ("paymentType",),
        })
    ]
    inlines = [
        PaymentInline,
    ]


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Регистрация модели оплаты в админке."""
    
    list_display = ("pk", "number", "month", "year", "code")
    fields = ["name", "number", "month", "year", "code", "order"]
    
