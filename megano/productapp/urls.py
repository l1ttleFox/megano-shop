from django.urls import path
from productapp import views

urlpatterns = [
    path("catalog/", views.CatalogView.as_view(), name="catalog"),
    path("categories/", views.CategoriesView.as_view(), name="categories"),
    path(
        "products/popular/",
        views.PopularProductsView.as_view(),
        name="popular_products",
    ),
    path(
        "products/limited/",
        views.LimitedProductsView.as_view(),
        name="limited_products",
    ),
    path("sales/", views.SaleItemView.as_view(), name="sales"),
    path("banners/", views.BannerView.as_view(), name="banners"),
    path(
        "product/<int:id>/", views.ProductsDetailView.as_view(), name="product_details"
    ),
    path(
        "product/<int:id>/reviews/",
        views.ReviewCreateView.as_view(),
        name="review_create",
    ),
    path("tags/", views.TagsView.as_view(), name="tags"),
]
