from django.contrib import admin
from productapp import models
from orderapp.admin import OrderProductInline


class TagInline(admin.TabularInline):
    model = models.Tag
    

class ProductTagInline(admin.TabularInline):
    model = models.Tag.products.through


class ProductSpecificationInline(admin.TabularInline):
    model = models.Specification.products.through
    

class ReviewInline(admin.TabularInline):
    model = models.Review
    

class SaleItemInline(admin.TabularInline):
    model = models.SaleItem


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    """Регистрация модели картинки в админке."""
    
    list_display = ("id", "alt")
    fields = ["alt", "src"]
    list_filter = ("alt",)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация модели категории в админке."""
    
    list_display = ("pk", "name")
    fields = ["name", ]
    list_filter = ("name", )
    list_display_links = ("pk", "name")
    inlines = [
        TagInline,
    ]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """Регистрация модели метки в админке."""
    
    list_display = ("id", "name", "category")
    fields = ["name", "category"]
    list_filter = ("name", )
    list_display_links = ("id", "name")
    inlines = [
        ProductTagInline,
    ]
    

@admin.register(models.CatalogItems)
class CatalogItems(admin.ModelAdmin):
    """Регистрация модели каталога товаров в админке."""
    
    list_display = ("id", "title", "main", "category")
    fields = ["title", "image", "main", "category", "subcategories"]
    list_filter = ("title", )
    list_display_links = ("id", "title")
    

@admin.register(models.Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """Регистрация модели спецификации в админке."""
    
    list_display = ("id", "name", "value")
    fields = ["name", "value"]
    list_filter = ("name", )
    list_display_links = ("id", "name")
    inlines = [
        ProductSpecificationInline,
    ]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """Регистрация модели продукта в админке."""
    
    list_filter = ("id", "count", "date")
    search_fields = ("title", "description", "fullDescription")
    list_display = ("id", "title", "count", "date")
    list_display_links = ("id", "title")
    fieldsets = [
        ("Base info", {
            "fields": ("title", "price", "count", "description", "images", "available"),
        }),
        ("Detail info", {
            "fields": ("fullDescription", "specifications", "tags", "category"),
            "classes": ("wide",),
        }),
        ("Options", {
            "fields": ("limited", "freeDelivery"),
        })
    ]
    inlines = [
        OrderProductInline,
        ReviewInline,
        SaleItemInline,
    ]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """Регистрация модели отзыва на товар в админке."""
    
    list_display = ("id", "author", "rate", "product")
    fields = ["author", "text", "rate", "product"]
    list_filter = ("rate", "date")
    search_fields = ("text", )


@admin.register(models.SaleItem)
class SaleItem(admin.ModelAdmin):
    """Регистрация модели товара со скидкой в админке."""
    
    list_display = ("id", "product", "salePrice", "dateFrom", "dateTo")
    fields = ["product", "salePrice", "dateFrom", "dateTo"]
    list_filter = ("salePrice", "dateFrom", "dateTo")
