from django.contrib.auth.models import User
from django.db import models


class Avatar(models.Model):
    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"
        
    src = models.ImageField(upload_to="media/users/avatars/", verbose_name="url")
    alt = models.CharField(max_length=100, blank=True, verbose_name="description")


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
    
    
class Profile(models.Model):
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="user")
    fullname = models.CharField(max_length=100, blank=True, verbose_name="full name")
    email = models.CharField(max_length=100, blank=True, verbose_name="email")
    phone = models.CharField(max_length=100, blank=True, unique=True, verbose_name="phone number")
    avatar = models.OneToOneField(Avatar, blank=True, on_delete=models.CASCADE, related_name="profile", verbose_name="avatar")
    

class Payment(models.Model):
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        
    number = models.CharField(max_length=100, blank=True, verbose_name="number")
    name = models.CharField(max_length=100, blank=True, verbose_name="name")
    month = models.CharField(max_length=100, blank=True, verbose_name="month")
    year = models.CharField(max_length=100, blank=True, verbose_name="year")
    code = models.CharField(max_length=100, blank=True, verbose_name="code")
    

class CatalogItem(models.Model):
    class Meta:
        verbose_name = "Item catalog"
        verbose_name_plural = "Item catalogs"
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, verbose_name="title")
    image = models.OneToOneField(Image, related_name="catalogitem", on_delete=models.CASCADE, verbose_name="image")
    

class CatalogItems(models.Model):
    class Meta:
        verbose_name = "Item catalog"
        verbose_name_plural = "Item catalogs"
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, verbose_name="title")
    image = models.OneToOneField(Image, related_name="catalogitems", on_delete=models.CASCADE, verbose_name="image")
    subcategories = models.ManyToManyField(CatalogItem, related_name="catalogitems", verbose_name="subcategories")
    
    
class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    id = models.AutoField(primary_key=True)
    category = models.IntegerField (max_length=100, blank=False, verbose_name="category")
    price = models.DecimalField(max_length=14, decimal_places=2, blank=False, verbose_name="price")
    count = models.IntegerField(max_length=100, blank=False, verbose_name="count")                      # это кол-во товара в магазине, или в корзине покупателя
    date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="date")
    title = models.CharField(max_length=100, blank=False, verbose_name="title")
    description = models.TextField(max_length=1000, blank=True, verbose_name="description")
    fullDescription = models.TextField(max_length=10000, blank=True, verbose_name="full description")
    freeDelivery = models.BooleanField(default=False, blank=True, verbose_name="free delivery")
    images = models.ManyToManyField(Image, related_name="products", blank=True, verbose_name="tags")
    tags = models.ManyToManyField(Tag, related_name="products", blank=True, verbose_name="tags")
    reviews = models.PositiveSmallIntegerField(blank=True, verbose_name="reviews")
    rating = models.DecimalField(decimal_places=1, blank=True, verbose_name="rating")
    
    
class Order(models.Model):
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        
    id = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False, verbose_name="created at")
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE, verbose_name="user")
    deliveryType = models.CharField(max_length=100, blank=True, verbose_name="delivery type")
    paymentType = models.CharField(max_length=100, blank=True, verbose_name="payment type")
    status = models.CharField(max_length=100, blank=True, verbose_name="status")
    city = models.CharField(max_length=100, blank=True, verbose_name="city")
    address = models.CharField(max_length=300, blank=True, verbose_name="address")
    products = models.ManyToManyField(Product, related_name="orders", verbose_name="products")
    # add to serializer: totalCost
    
    
class SaleItem(models.Model):
    class Meta:
        verbose_name = "sale item"
        verbose_name_plural = "sale items"
        
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name="sales", verbose_name="products", on_delete=models.CASCADE)
    dateFrom = models.DateTimeField(auto_now_add=True, verbose_name="date from")
    dateTo = models.DateTimeField(verbose_name="date to")
    # add to serializer: price, salePrice, title, images
    
    
