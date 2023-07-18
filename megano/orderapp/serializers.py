from time import strftime
from rest_framework import serializers
from orderapp.models import Payment, Order
from orderapp.models import OrderProduct
from productapp.serializers import ImageSerializer, TagSerializer


class PaymentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = ["number", "name", "month", "year", "code"]
        
    def get_name(self, obj):
        return obj.user.profile.fullname
    
    def get_month(self, obj):
        return obj.created_date.strftime("%m")
    
    def get_year(self, obj):
        return obj.created_date.strftime("%Y")
    
    
class OrderProductSerializer(serializers.ModelSerializer):
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
        return round(obj.product.real_price() * obj.count, 2)
    
    def get_category(self, obj):
        return obj.product.category
    
    def get_date(self, obj):
        return obj.product.date
    
    def get_title(self, obj):
        return obj.product.title
    
    def get_description(self, obj):
        return obj.product.description
    
    def get_freeDelivery(self, obj):
        return obj.product.freeDelivery
    
    
class OrderSerializer(serializers.ModelSerializer):
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
        return obj.user.profule.fullname
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_phone(self, obj):
        return obj.user.profile.phone
    
    def get_deliveryType(self, obj):
        if not obj.deliveryType:
            if all(obj.products.freeDelivery):
                return "free"
            return "extra cost"
        return obj.deliveryType
    
    def get_totalCost(self, obj):
        return sum([i_product.price for i_product in obj.products])