from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import FoodgramUser, Subscribe
from recipes.models import  Recipe


class FoodgramUserSerializer(UserSerializer):
    """Сериализатор пользователя, модели FoodgramUser."""

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
    
    def get_is_subscribed(self, following):
        if self.context.get('request',).user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=self.context.get('request').user,
            following=following
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
    """Сериализация списка на кого подписан пользователь"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = FoodgramUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
    
    def get_is_subscribed(self, following):
        if self.context.get('request',).user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=self.context.get('request').user,
            following=following
        ).exists()
    
    def get_recipes(self, following):
        queryset = self.context.get('request')
        recipes_limit = queryset.query_params.get('recipes_limit')
        if not recipes_limit:
            return RecipeFollowingSerializer(
                following.author.all(),
                many=True, context={'request': queryset}
            ).data
        return RecipeFollowingSerializer(
            following.author.all()[:int(recipes_limit)], many=True,
            context={'request': queryset}
        ).data

    def get_recipes_count(self, following):
        return Recipe.objects.filter(author=following).count()


class RecipeFollowingSerializer(serializers.ModelSerializer):
    """Сериализация списка рецептов авторов, на которых подписан пользователь"""
    
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowSerializer(serializers.ModelSerializer):
    """Сериализация при подписке"""
    class Meta:
        model = Subscribe
        fields = ('user', 'following')

    def validate(self, data):
        get_object_or_404(FoodgramUser, username=data['following'])
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError('Нельзя подписываться на самого себя!')
        if Subscribe.objects.filter(
                user=self.context['request'].user,
                following=data['following']
        ):
            raise serializers.ValidationError('Вы уже подписаны на этого пользователя.')
        return data

    def to_representation(self, instance):
        return FollowListSerializer(
            instance.following,
            context={'request': self.context.get('request')}
        ).data