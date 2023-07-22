from django.contrib.auth.models import User
from django.db import models
from productapp.models import Product


class Payment(models.Model):
    """ Модель оплаты заказа. """
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="payments", verbose_name="user")
    number = models.CharField(max_length=100, blank=True, verbose_name="number")
    created_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=100, blank=True, verbose_name="code")


class Basket(models.Model):
    """
    Модель корзины товаров.
    Основные поля описаны через внешний ключ.
    """
    
    class Meta:
        verbose_name = "basket"
        verbose_name_plural = "baskets"


class OrderProduct(models.Model):
    """ Модель товара в заказе. """
    
    class Meta:
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"
    
    id = models.AutoField(primary_key=True)
    count = models.IntegerField(blank=False, verbose_name="count")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, default=None, related_name="order_products", verbose_name="product")
    basket = models.ForeignKey(Basket, on_delete=models.PROTECT, default=None, related_name="order_products", verbose_name="basket")
    
    @property
    def rating(self):
        """ Геттер рейтинга товара для сериализатора. """
        
        self.review_list = [i_review.rate for i_review in self.reviews]
        return round(sum(self.review_list) / len(self.review_list), 2)
    
    @property
    def price(self):
        """ Геттер общей стоимости товаров с одинаковым ID для сериализатора. """
        
        if self.product.saleitem:
            return round(int(self.count) * float(self.product.saleitem.salePrice), 2)
        return round(int(self.count) * float(self.product), 2)


class Order(models.Model):
    """ Модель заказа. """
    
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
