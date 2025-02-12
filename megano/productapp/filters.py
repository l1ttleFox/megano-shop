from django.db.models import Count, Avg
from rest_framework import filters


class CatalogFilter(filters.BaseFilterBackend):
    """Кастомный фильтр для сортировки запроса каталога."""

    def filter_queryset(self, request, queryset, view):
        sort = request.GET.get("sort", "date")
        sort_type = request.GET.get("sortType", None)

        if sort == "reviews":
            queryset = queryset.annotate(reviews_count=Count("reviews")).order_by(
                "reviews_count"
            )
        elif sort == "rating":
            queryset = queryset.annotate(_rating=Avg("reviews__rate")).order_by(
                "_rating"
            )
        else:
            queryset = queryset.order_by(f"{sort}")
        if sort_type != "inc":
            queryset = queryset.reverse()

        return queryset
