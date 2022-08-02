from rest_framework.pagination import PageNumberPagination

class ApiPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'limit'