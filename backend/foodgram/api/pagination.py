from rest_framework.pagination import PageNumberPagination

class UsersApiPagination(PageNumberPagination):
    page_size = 6