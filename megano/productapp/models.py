from django.contrib.auth.models import User
from django.db import models
import datetime


class Image(models.Model):
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Image"

    src = models.ImageField(upload_to="media/images/", verbose_name="url")
    alt = models.CharField(max_length=100, blank=True, verbose_name="description")


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, unique=True, verbose_name="name")


class CatalogItems(models.Model):
    class Meta:
        verbose_name = "Item Catalogs"
        verbose_name_plural = "Items Catalogs"
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, verbose_name="title")
    image = models.OneToOneField(Image, related_name="catalogitems", on_delete=models.PROTECT, verbose_name="image")
    subcategories = models.ManyToManyField("productapp.CatalogItems", related_name="catalogitems", verbose_name="subcategories")


class Specification(models.Model):
    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"
    
    name = models.CharField(max_length=300, blank=True, verbose_name="name")
    value = models.CharField(max_length=100, blank=True, verbose_name="value")


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    id = models.AutoField(primary_key=True)
    category = models.IntegerField(blank=False, verbose_name="category")
    price = models.DecimalField(max_digits=14, decimal_places=2, blank=False, verbose_name="price")
    count = models.IntegerField(blank=False, verbose_name="count")  # это кол-во товара в магазине, или в корзине покупателя?
    date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="date")
    title = models.CharField(max_length=100, blank=False, verbose_name="title")
    description = models.TextField(max_length=1000, blank=True, verbose_name="description")
    fullDescription = models.TextField(max_length=10000, blank=True, verbose_name="full description")
    freeDelivery = models.BooleanField(default=False, blank=True, verbose_name="free delivery")
    images = models.ManyToManyField(Image, related_name="products", blank=True, verbose_name="tags")
    tags = models.ManyToManyField(Tag, related_name="products", blank=True, verbose_name="tags")
    specifications = models.ManyToManyField(Specification, related_name="products", verbose_name="specifications")
    
    @property
    def rating(self):
        self.review_list = [i_review.rate for i_review in self.reviews]
        return round(sum(self.review_list) / len(self.review_list), 2)
    
    @property
    def real_price(self):
        if self.saleitem:
            if self.saleitem.dateFrom < datetime.datetime.now() < self.saleitem.dateTo:
                return self.saleitem.salePrice
        return self.price


class Review(models.Model):
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
    
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="reviews", verbose_name="review")
    text = models.TextField(max_length=5000, blank=True, verbose_name="text")
    rate = models.PositiveSmallIntegerField(blank=True, verbose_name="rate")
    date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="product")
    
    @property
    def email(self):
        return self.author.email
    
    @property
    def author_name(self):
        if self.author.first_name:
            return self.author.first_name
        return self.author.username
    

class SaleItem(models.Model):
    class Meta:
        verbose_name = "Sale Item"
        verbose_name_plural = "Sale Items"

    id = models.AutoField(primary_key=True)
    product = models.OneToOneField(Product, on_delete=models.PROTECT, related_name="saleitem", verbose_name="product")
    salePrice = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="sale price")
    dateFrom = models.DateTimeField(auto_now_add=True, verbose_name="date from")
    dateTo = models.DateTimeField(verbose_name="date to")
