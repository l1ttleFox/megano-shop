from time import strftime
from rest_framework import serializers
from orderapp.models import Payment, Order
from orderapp.models import OrderProduct
from productapp.serializers import ImageSerializer, TagSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """ Сериализатор модели оплаты заказа. """
    
    name = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = ["number", "name", "month", "year", "code"]
        
    def get_name(self, obj):
        """ Метод определения поля имени заказчика вручную. """
        return obj.user.profile.fullname
    
    def get_month(self, obj):
        """ Метод определения поля месяца оплаты вручную. """
        return obj.created_date.strftime("%m")
    
    def get_year(self, obj):
        """ Метод определения года оплаты вручную. """
        return obj.created_date.strftime("%Y")
    
    
class OrderProductSerializer(serializers.ModelSerializer):
    """ Сериализатор модели продукта в заказе. """
    
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    rating = serializers.ReadOnlyField(source="rating")
    price = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    freeDelivery = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderProduct
        field = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating"
        ]
    
    def get_price(self, obj):
        """ Метод определения поля общей стоимости товара вручную. """
        return round(obj.product.real_price() * obj.count, 2)
    
    def get_category(self, obj):
        """ Метод определения поля категории товара вручную. """
        return obj.product.category
    
    def get_date(self, obj):
        """ Метод определения поля даты публикации товара вручную. """
        return obj.product.date
    
    def get_title(self, obj):
        """ Метод определения поля заголовка товара вручную. """
        return obj.product.title
    
    def get_description(self, obj):
        """ Метод определения поля описания товара вручную. """
        return obj.product.description
    
    def get_freeDelivery(self, obj):
        """ Метод определения поля доставки товара вручную. """
        return obj.product.freeDelivery
    
    
class OrderSerializer(serializers.ModelSerializer):
    """ Сериализатор модели заказа. """
    
    products = OrderProductSerializer(many=True)
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    deliveryType = serializers.SerializerMethodField()
    totalCost = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            "id",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products"
        ]
        
    def get_fullName(self, obj):
        """ Метод определения поля имени заказчика вручную. """
        return obj.user.profule.fullname
    
    def get_email(self, obj):
        """ Метод определения поля электронной почты заказчика вручную. """
        return obj.user.email
    
    def get_phone(self, obj):
        """ Метод определения поля номера телефона заказчика вручную. """
        return obj.user.profile.phone
    
    def get_deliveryType(self, obj):
        """ Метод определения поля доставки заказа вручную. """
        if not obj.deliveryType:
            if all(obj.products.freeDelivery):
                return "free"
            return "extra cost"
        return obj.deliveryType
    
    def get_totalCost(self, obj):
        """ Метод определения поля общей стоимости заказа вручную. """
        return sum([i_product.price for i_product in obj.products])
    
    
