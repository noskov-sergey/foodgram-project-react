from djoser.views import UserViewSet
from rest_framework import filters, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import FoodgramUser
from .serializers import FoodgramUserSerializer, FollowListSerializer
from api.pagination import UsersApiPagination

class FoodgramUserViewSet(UserViewSet):
    pagination_class = UsersApiPagination

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
    
    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request, pk=None):
        subscriptions_users = self.paginate_queryset(
            FoodgramUser.objects.filter(following__user=request.user)
        )
        serializer = FollowListSerializer(
            subscriptions_users,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)


    @action(
        detail=True,
        methods=['POST'],
        permission_classes=(IsAuthenticated, )
    )
    def subscribe(self, request, pk=None):
        subscriptions_users = self.paginate_queryset(
            FoodgramUser.objects.filter(following__user=request.user)
        )
        serializer = FollowListSerializer(
            subscriptions_users,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)
