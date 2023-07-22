from rest_framework import serializers

from productapp.models import (
    CatalogItems,
    Image,
    Tag,
    Specification,
    Review,
    Product,
    SaleItem
)


class ImageSerializer(serializers.ModelSerializer):
    """ Сериализатор модели изображения товара. """
    
    class Meta:
        model = Image
        fields = ["src", "alt"]


class CatalogItemsSerializer(serializers.ModelSerializer):
    """ Сериализатор модели каталога товаров. """
    
    image = ImageSerializer(many=True)
    
    class Meta:
        model = CatalogItems
        fields = ["id", "title", "image", "subcategories"]
        depth = 1
        

class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор модели категории товара. """
    
    class Meta:
        model = Tag
        fields = ["id", "name"]
        
        
class SpecificationSerializer(serializers.ModelSerializer):
    """ Сериализатор модели спецификации товара. """
    
    class Meta:
        model = Specification
        fields = ["name", "value"]
        

class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализатор модели отзыва на товар. """
    
    author = serializers.ReadOnlyField(source="author_name")
    email = serializers.ReadOnlyField(source="email")
    
    class Meta:
        model = Review
        fields = ["author", "email", "text", "rate", "date"]
    

class ProductFullSerializer(serializers.ModelSerializer):
    """ Полный сериализатор модели товара. """
    
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    specifications = SpecificationSerializer(many=True)
    rating = serializers.ReadOnlyField(source="rating")
    reviews = serializers.SerializerMethodField()
    
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
            "rating"
        ]
        
    def get_reviews(self, obj):
        """ Метод определения поля отзывов на товар вручную. """
        selected_reviews = obj.reviews.all()
        return ReviewSerializer(selected_reviews, many=True).data
    

class ProductShortSerializer(serializers.ModelSerializer):
    """ Неполный сериализатор модели товара. """
    
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    rating = serializers.ReadOnlyField(source="rating")
    reviews = serializers.SerializerMethodField()
    
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
            "rating"
        ]
    
    def get_reviews(self, obj):
        """ Метод определения поля отзывов на товар вручную. """
        selected_reviews = obj.reviews.all()
        return ReviewSerializer(selected_reviews, many=True).data


class SaleItemSerializer(serializers.ModelSerializer):
    """ Сериализатор модели товара со скидкой. """
    
    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = SaleItem
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]
        
    def get_price(self, obj):
        """ Метод определения поля цены товара со скидкой вручную. """
        return obj.product.price
    
    def get_title(self, obj):
        """ Метод определения поля названия товара со скидкой вручную. """
        return obj.product.title
    
    def get_images(self, obj):
        """ Метод определения поля изображения товара вручную. """
        selected_images = obj.images.all()
        return ImageSerializer(selected_images, many=True).data
        
    