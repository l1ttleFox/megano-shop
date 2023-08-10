from rest_framework import serializers
from productapp.models import (
    CatalogItems,
    Image,
    Tag,
    Specification,
    Review,
    Product,
    SaleItem,
)


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор модели изображения товара."""

    class Meta:
        model = Image
        fields = ["src", "alt"]


class CatalogItemSerializer(serializers.ModelSerializer):
    """"""
    
    image = ImageSerializer()
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = CatalogItems
        fields = ["id", "title", "image"]
    
    def get_id(self, obj):
        """ Метод получения поля id категории вручную."""
        return obj.category.pk


class CatalogItemsSerializer(serializers.ModelSerializer):
    """Сериализатор модели каталога товаров."""

    image = ImageSerializer()
    id = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = CatalogItems
        fields = ["id", "title", "image", "subcategories"]
        
    def get_id(self, obj):
        """ Метод получения поля id категории вручную."""
        return obj.category.pk
    
    def get_subcategories(self, obj):
        """ Метод получения поля подкатегорий вручную."""
        subcategories = obj.subcategories.all()
        return CatalogItemSerializer(subcategories, many=True).data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели метки товара."""

    class Meta:
        model = Tag
        fields = ["id", "name"]


class SpecificationSerializer(serializers.ModelSerializer):
    """Сериализатор модели спецификации товара."""

    class Meta:
        model = Specification
        fields = ["name", "value"]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзыва на товар."""

    author = serializers.ReadOnlyField(source="author_name")
    email = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField(source="cute_date")

    class Meta:
        model = Review
        fields = ["author", "email", "text", "rate", "date"]


class ProductFullSerializer(serializers.ModelSerializer):
    """Полный сериализатор модели товара."""

    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    specifications = SpecificationSerializer(many=True)
    rating = serializers.ReadOnlyField()
    reviews = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]

    def get_reviews(self, obj):
        """Метод определения поля отзывов на товар вручную."""
        selected_reviews = obj.reviews.all()
        return ReviewSerializer(selected_reviews, many=True).data

    def get_category(self, obj):
        """ Метод получения поля id категории вручную."""
        return obj.category.pk


class ProductShortSerializer(serializers.ModelSerializer):
    """Неполный сериализатор модели товара."""

    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    rating = serializers.ReadOnlyField()
    price = serializers.ReadOnlyField(source="real_price")
    reviews = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
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

    def get_reviews(self, obj):
        """Метод определения поля отзывов на товар вручную."""
        selected_reviews = obj.reviews.all()
        return ReviewSerializer(selected_reviews, many=True).data

    def get_category(self, obj):
        """ Метод получения поля id категории вручную."""
        return obj.category.pk


class SaleItemSerializer(serializers.ModelSerializer):
    """Сериализатор модели товара со скидкой."""

    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]
        
    def get_dateTo(self, obj):
        """ Метод получения поля даты окончания скидки вручную."""
        return obj.dateTo.strftime("%m-%d")

    def get_dateFrom(self, obj):
        """ Метод получения поля даты начала скидки вручную."""
        return obj.dateFrom.strftime("%m-%d")
        
    def get_id(self, obj):
        """ Метод получения поля id продукта вручную."""
        return obj.product.id

    def get_price(self, obj):
        """Метод определения поля цены товара со скидкой вручную."""
        return obj.product.price

    def get_title(self, obj):
        """Метод определения поля названия товара со скидкой вручную."""
        return obj.product.title

    def get_images(self, obj):
        """Метод определения поля изображения товара вручную."""
        selected_images = obj.product.images.all()
        return ImageSerializer(selected_images, many=True).data
