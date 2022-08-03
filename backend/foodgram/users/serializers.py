from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from .models import FoodgramUser, Subscribe


class FoodgramUserSerializer(UserSerializer):
    """Сериализатор пользователя, модели User."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model = FoodgramUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
    
    def get_is_subscribed(self, author):
        if self.context.get('request',).user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=self.context.get('request').user,
            author=author
        ).exists()


class FoodgramUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = FoodgramUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class FollowListSerializer(serializers.ModelSerializer):
    """ Сериализация списка на кого подписан пользователь"""

    class Meta:
        model = FoodgramUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
        )