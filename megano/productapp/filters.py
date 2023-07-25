from django.db.models import Count, Avg
from rest_framework import filters


class CatalogFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        sort = request.GET.get("sort", "date")
        sort_type = request.GET.get("sortType", None)
            
        if sort != "date":
            if sort == "reviews":
                queryset = queryset.annotate(reviews_count=Count("tags")).order_by("reviews_count")
                return queryset
            if sort == "rating":
                queryset = queryset.annontate(product_rating=Avg("reviews__rate")).filter("product_rating")
                return queryset
        
        queryset = queryset.order_by(f"{sort}")
        if sort_type != "inc":
            queryset = queryset.reverse()

        return queryset
    