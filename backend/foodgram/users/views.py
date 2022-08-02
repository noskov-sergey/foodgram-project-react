from djoser.views import UserViewSet
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import FoodgramUser
from .serializers import FoodgramUserSerializer
from api.pagination import ApiPagination

class FoodgramUserViewSet(UserViewSet):
    paginationclass = ApiPagination

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated, )
    )
    def users(self, request):
        serializer = FoodgramUserSerializer(
            super().get_queryset(), many=True, context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)
