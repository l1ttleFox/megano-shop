import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from orderapp.models import Payment, Order
from orderapp.models import OrderProduct
from productapp.serializers import ImageSerializer, TagSerializer, ReviewSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор модели оплаты заказа."""

    class Meta:
        model = Payment
        fields = ["number", "name", "month", "year", "code"]


class OrderProductSerializer(serializers.ModelSerializer):
    """Сериализатор модели продукта в заказе."""

    images = ImageSerializer(many=True, source="product.images")
    tags = TagSerializer(many=True, source="product.tags")
    rating = serializers.ReadOnlyField()
    price = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    freeDelivery = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = [
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
            "rating",
        ]

    def get_price(self, obj):
        """Метод определения поля общей стоимости товара вручную."""
        return obj.product.real_price * obj.count

    def get_category(self, obj):
        """Метод определения поля категории товара вручную."""
        return obj.product.category.id

    def get_date(self, obj):
        """Метод определения поля даты публикации товара вручную."""
        return obj.product.date

    def get_title(self, obj):
        """Метод определения поля заголовка товара вручную."""
        return obj.product.title

    def get_description(self, obj):
        """Метод определения поля описания товара вручную."""
        return obj.product.description

    def get_freeDelivery(self, obj):
        """Метод определения поля доставки товара вручную."""
        return obj.product.freeDelivery

    def get_reviews(self, obj):
        """Метод определения поля отзывов вручную."""
        reviews = [i_review for i_review in obj.product.reviews.all()]
        serialized_data = ReviewSerializer(reviews, many=True).data
        return serialized_data


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор модели заказа."""

    products = serializers.SerializerMethodField()
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
            "products",
        ]

    def get_products(self, obj):
        """Метод определения поля продуктов вручную."""
        order_products = [
            i_order_product for i_order_product in obj.basket.order_products.all()
        ]
        serialized_data = OrderProductSerializer(order_products, many=True).data
        return serialized_data

    def get_fullName(self, obj):
        """Метод определения поля имени заказчика вручную."""
        return obj.user.profile.fullname

    def get_email(self, obj):
        """Метод определения поля электронной почты заказчика вручную."""
        return obj.user.email

    def get_phone(self, obj):
        """Метод определения поля номера телефона заказчика вручную."""
        return obj.user.profile.phone

    def get_deliveryType(self, obj):
        """Метод определения поля доставки заказа вручную."""
        if not obj.deliveryType:
            if all(obj.products.freeDelivery):
                return "free"
            return "extra cost"
        return obj.deliveryType

    def get_totalCost(self, obj):
        """Метод определения поля общей стоимости заказа вручную."""
        return sum([i_product.price for i_product in obj.basket.order_products.all()])


class ShortOrderSerializer(serializers.ModelSerializer):
    """Краткий сериализатор модели заказа."""

    orderId = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "orderId",
        ]

    def get_orderId(self, obj):
        """Метод определения id заказа вручную."""
        return obj.id


class OrderProductInBasketSerializer(serializers.ModelSerializer):
    """Неполный сериализатор модели товара."""

    id = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, source="product.images")
    tags = TagSerializer(many=True, source="product.tags")
    rating = serializers.ReadOnlyField()
    price = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    freeDelivery = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = [
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
            "rating",
        ]

    def get_id(self, obj):
        """Метод получения id товара вручную."""
        return obj.product.id

    def get_reviews(self, obj):
        """Метод определения поля отзывов на товар вручную."""
        selected_reviews = obj.product.reviews.all()
        return ReviewSerializer(selected_reviews, many=True).data

    def get_category(self, obj):
        """Метод получения категории товара вручную."""
        return obj.product.category.pk

    def get_date(self, obj):
        """Метод получения даты публикации товара вручную."""
        return obj.product.date

    def get_title(self, obj):
        """Метод получения названия товара вручную."""
        return obj.product.title

    def get_description(self, obj):
        """Метод получения описания товара вручную."""
        return obj.product.description

    def get_freeDelivery(self, obj):
        """Метод получения поля доставки товара вручную."""
        return obj.product.freeDelivery

    def get_price(self, obj):
        """Метод получения поля цены товара вручную."""
        try:
            if (
                obj.product.saleitem.dateFrom
                < datetime.datetime.now()
                < obj.product.saleitem.dateTo
            ):
                price = obj.product.saleitem.salePrice
        except ObjectDoesNotExist:
            price = obj.product.price
        return price
