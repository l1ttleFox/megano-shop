from django.db.models import Count
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from productapp import serializers
from productapp import models
import json
from productapp.filters import CatalogFilter
from productapp.pagination import CatalogPagination, SaleItemsPagination


class CategoriesView(ListAPIView):
    """View категорий товаров."""

    queryset = models.CatalogItems.objects.all()
    serializer_class = serializers.CatalogItemsSerializer


class CatalogView(ListAPIView):
    """View каталога товаров."""

    serializer_class = serializers.ProductShortSerializer
    filter_backends = [CatalogFilter]
    pagination_class = CatalogPagination

    def get_queryset(self):
        """Метод получения запроса к бд вручную с учётом всех фильтров."""

        queryset = models.Product.objects.all()

        name = self.request.GET.get("filter[name]", None)
        if name:
            queryset = queryset.filter(title__contains=name)

        min_price = self.request.GET.get("filter[minPrice]", None)
        max_price = self.request.GET.get("filter[maxPrice]", None)
        if min_price and max_price:
            queryset = queryset.filter(price__range=(int(min_price), int(max_price)))
        elif min_price:
            queryset = queryset.filter(price__gte=int(min_price))
        elif max_price:
            queryset = queryset.filter(price__lte=int(max_price))

        free_delivery = self.request.GET.get("filter[freeDelivery]", None)
        if free_delivery:
            if free_delivery == "true":
                free_delivery = True
            elif free_delivery == "false":
                free_delivery = False
            queryset = queryset.filter(free_delivery=free_delivery)

        available = self.request.GET.get("filter[available]", None)
        if available:
            if available == "true":
                available = True
            elif available == "false":
                available = False
            queryset = queryset.filter(available=available)

        category = self.request.GET.get("category", None)
        if category:
            queryset = queryset.filter(category=category)

        tags = json.loads(self.request.GET.get("tags", None))
        if tags:
            tag_ids = [int(i_tag["id"]) for i_tag in tags]
            tags = models.Tag.objects.filter(pk__in=tag_ids)
            queryset = queryset.filter(tags__in=tags)

        return queryset


class PopularProductsView(ListAPIView):
    """View популярных продуктов."""

    serializer_class = serializers.ProductShortSerializer

    def get_queryset(self):
        """Метод получения запроса к бд вручную."""
        queryset = models.Product.objects.filter(available=True).all()
        queryset = queryset.annotate(orders_count=Count("orders")).order_by(
            "-orders_count"
        )[: int(models.Product.objects.count() / 10)]
        return queryset


class LimitedProductsView(ListAPIView):
    """View лимитированных продуктов."""

    serializer_class = serializers.ProductShortSerializer
    queryset = models.Product.objects.filter(limited=True, available=True).all()


class SaleItemView(ListAPIView):
    """View продуктов со скидкой."""

    serializer_class = serializers.SaleItemSerializer
    queryset = models.SaleItem.objects.all()
    pagination_class = SaleItemsPagination


class BannerView(ListAPIView):
    """View списка продуктов."""

    serializer_class = serializers.ProductShortSerializer
    queryset = models.Product.objects.filter(available=True).all()


class ProductsDetailView(RetrieveAPIView):
    """View детального отображения продукта."""

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductFullSerializer


class ReviewCreateView(CreateAPIView):
    """View создания отзыва на товар."""

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        """Метод добавления товара к отзыву."""
        selected_product = models.Product.objects.get(id=self.kwargs["id"])
        serializer.save(product=selected_product)
        serializer.save()


class TagsView(ListAPIView):
    """View меток товаров."""

    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Метод получения запроса к бд вручную."""
        queryset = models.Tag.objects.all()

        category = self.request.GET.get("category", 123)
        queryset = queryset.filter(category=category)

        return queryset
