from django.contrib import admin
from productapp import models


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "alt")
    fields = ["id", "alt", "src"]
    list_filter = ("alt",)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    fields = ["id", "name", "products"]
    list_filter = ("id", "name")


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    fields = ["id", "name", "category", "products"]
    list_filter = ("id", "name")
    

@admin.register(models.CatalogItems)
class CatalogItems(admin.ModelAdmin):
    list_display = ("id", "title")
    fields = ["id", "title", "image", "subcategories"]
    list_filter = ("id", "title")
    

@admin.register(models.Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value")
    fields = ["id", "name", "value"]
    list_filter = ("id", "name")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ("id", "count", "date")
    search_fields = ("title", "description", "fullDescription")
    fieldsets = [
        ("Base info", {
            "fields": ("id", "price", "count", "description", "images", "available"),
        }),
        ("Detail info", {
            "fields": ("date", "fullDescription", "specifications", "tags", "category"),
            "classes": ("wide",),
        }),
        ("Options", {
            "fields": ("limited", "freeDelivery"),
        })
    ]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "rate", "date", "product")
    fields = ["author", "text", "rate", "date", "product"]
    list_filter = ("rate", "date")
    search_fields = ("text", )


@admin.register(models.SaleItem)
class SaleItem(admin.ModelAdmin):
    list_display = ("id", "product", "salePrice", "dateFrom", "dateTo")
    fields = ["id", "product", "salePrice", "dateFrom", "dateTo"]
    list_filter = ("id", "salePrice", "dateFrom", "dateTo")
