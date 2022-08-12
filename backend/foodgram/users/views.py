from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FoodgramUser, Subscribe
from .serializers import (FollowListSerializer, FollowSerializer,
                          FoodgramUserSerializer)
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

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        if request.method != 'POST':
            subscription = get_object_or_404(
                Subscribe,
                following=get_object_or_404(FoodgramUser, id=id),
                user=request.user
            )
            self.perform_destroy(subscription)
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = FollowSerializer(
            data={
                'user': request.user.id,
                'following': get_object_or_404(FoodgramUser, id=id).id
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
