from django.contrib.auth.models import User
from django.db import models
import datetime


class Image(models.Model):
    """Модель картинки товара."""

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Image"
        ordering = ["id"]

    src = models.ImageField(upload_to="media/images/", verbose_name="url")
    alt = models.CharField(max_length=100, blank=True, verbose_name="description")


class Category(models.Model):
    """Модель категории товара."""

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    name = models.CharField(max_length=100, blank=True, verbose_name="name")


class Tag(models.Model):
    """Модель метки категории товара."""

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100, blank=True, unique=True, verbose_name="name"
    )
    category = models.ForeignKey(
        Category,
        related_name="tags",
        null=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="category",
    )


class CatalogItems(models.Model):
    """Модель каталога товаров."""

    class Meta:
        verbose_name = "Item Catalogs"
        verbose_name_plural = "Items Catalogs"
        ordering = ["title"]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, verbose_name="title")
    image = models.OneToOneField(
        Image,
        related_name="catalogitems",
        on_delete=models.PROTECT,
        verbose_name="image",
    )
    subcategories = models.ManyToManyField(
        "productapp.CatalogItems",
        related_name="catalogitems",
        verbose_name="subcategories",
    )


class Specification(models.Model):
    """Модель спецификаций товаров."""

    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"
        ordering = ["name"]

    name = models.CharField(max_length=300, blank=True, verbose_name="name")
    value = models.CharField(max_length=100, blank=True, verbose_name="value")


class Product(models.Model):
    """Модель продукта."""

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["title"]

    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        default=None,
        related_name="products",
        verbose_name="category",
    )
    price = models.DecimalField(
        max_digits=14, decimal_places=2, blank=False, verbose_name="price"
    )
    count = models.IntegerField(
        blank=False, verbose_name="count"
    )  # это кол-во товара в магазине, или в корзине покупателя?
    date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="date")
    title = models.CharField(max_length=100, blank=False, verbose_name="title")
    description = models.TextField(
        max_length=1000, blank=True, verbose_name="description"
    )
    fullDescription = models.TextField(
        max_length=10000, blank=True, verbose_name="full description"
    )
    freeDelivery = models.BooleanField(
        default=False, blank=True, verbose_name="free delivery"
    )
    images = models.ManyToManyField(
        Image, related_name="products", blank=True, verbose_name="tags"
    )
    tags = models.ManyToManyField(
        Tag, related_name="products", blank=True, verbose_name="tags"
    )
    specifications = models.ManyToManyField(
        Specification, related_name="products", verbose_name="specifications"
    )
    # extra fields
    limited = models.BooleanField(default=False, verbose_name="limited")
    available = models.BooleanField(default=True, verbose_name="available")
    
    def __str__(self):
        return f"{self.title} (id: {self.id}, price: {self.price})"
    
    @property
    def rating(self):
        """Геттер рейтинга товара для сериализатора."""

        self.review_list = [i_review.rate for i_review in self.reviews]
        return round(sum(self.review_list) / len(self.review_list), 2)

    @property
    def real_price(self):
        """Геттер цены товара для сериализатора."""

        if self.saleitem:
            if self.saleitem.dateFrom < datetime.datetime.now() < self.saleitem.dateTo:
                return self.saleitem.salePrice
        return self.price


class Review(models.Model):
    """Модель отзыва на товар."""

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-date"]

    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="reviews", verbose_name="review"
    )
    text = models.TextField(max_length=5000, blank=True, verbose_name="text")
    rate = models.PositiveSmallIntegerField(blank=True, verbose_name="rate")
    date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="product",
    )

    @property
    def email(self):
        """Геттер электронной почты пользователя для сериализатора."""

        return self.author.email

    @property
    def author_name(self):
        """Геттер имени пользователя для сериализатора."""

        if self.author.first_name:
            return self.author.first_name
        return self.author.username


class SaleItem(models.Model):
    """Модель товара со скидкой."""

    class Meta:
        verbose_name = "Sale Item"
        verbose_name_plural = "Sale Items"
        ordering = ["product"]
        
    id = models.AutoField(primary_key=True)
    product = models.OneToOneField(
        Product,
        on_delete=models.PROTECT,
        related_name="saleitem",
        verbose_name="product",
    )
    salePrice = models.DecimalField(
        max_digits=14, decimal_places=2, verbose_name="sale price"
    )
    dateFrom = models.DateTimeField(auto_now_add=True, verbose_name="date from")
    dateTo = models.DateTimeField(verbose_name="date to")
