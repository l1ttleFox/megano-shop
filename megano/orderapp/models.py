from django.contrib.auth.models import User
from django.db import models
from productapp.models import Product


class Payment(models.Model):
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="payments", verbose_name="user")
    number = models.CharField(max_length=100, blank=True, verbose_name="number")
    created_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=100, blank=True, verbose_name="code")


class OrderProduct(models.Model):
    class Meta:
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"
    
    id = models.AutoField(primary_key=True)
    count = models.IntegerField(blank=False, verbose_name="count")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_products", verbose_name="product")
    
    @property
    def rating(self):
        self.review_list = [i_review.rate for i_review in self.reviews]
        return round(sum(self.review_list) / len(self.review_list), 2)
    
    @property
    def price(self):
        return int(self.count) * float(self.product)


class Order(models.Model):
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    id = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False, verbose_name="created at")
    user = models.ForeignKey(User, related_name="orders", on_delete=models.PROTECT, verbose_name="user")
    deliveryType = models.CharField(max_length=100, blank=True, default=None, verbose_name="delivery type")
    paymentType = models.CharField(max_length=100, blank=True, verbose_name="payment type")
    status = models.CharField(max_length=100, blank=True, verbose_name="status")
    city = models.CharField(max_length=100, blank=True, verbose_name="city")
    address = models.CharField(max_length=300, blank=True, verbose_name="address")
    products = models.ManyToManyField(OrderProduct, related_name="orders", verbose_name="order_products")
    # add to serializer: totalCost

