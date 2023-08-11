from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """Кастомный класс пагинации для работы с фронтендом."""

    def get_paginated_response(self, data):
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            }
        )


class CatalogPagination(CustomPagination):
    """Пагинация для каталога."""

    page_size = 20
    page_size_query_param = "limit"
    page_query_param = "currentPage"


class SaleItemsPagination(CustomPagination):
    """Пагинация для товаров со скидкой."""

    page_size = 20
    page_query_param = "currentPage"
