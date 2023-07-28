from rest_framework.pagination import PageNumberPagination


class CatalogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    page_query_param = "currentPage"


class SaleItemsPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "currentPage"
