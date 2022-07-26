from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .convertors import Base64ImageField
from recipes.models import (Tag, Ingredient, Ingredients_Amount,
                            Recipe, Favorites, ShoppingCart)
from users.serializers import FoodgramUserSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов, модели Tag."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов, модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientDetailSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор промежуточной модели Ingredients_Amount"""
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )
    id = serializers.IntegerField(source='ingredient.id', read_only=True)

    class Meta:
        model = Ingredients_Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class GetRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта, модели Recipe."""

    author = FoodgramUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients',)
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited',
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart',
        read_only=True
    )

    class Meta:
        model = Recipe
        depth = 1
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, recipe):
        if self.context.get('request').user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=self.context.get('request').user,
            recipe=recipe
        ).exists()

    def get_is_in_shopping_cart(self, recipe):
        if self.context.get('request').user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=self.context.get('request').user,
            recipe=recipe
        ).exists()

    def get_ingredients(self, recipe):
        return IngredientDetailSerializer(
            Ingredients_Amount.objects.filter(recipe=recipe),
            many=True
        ).data

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['image'] = obj.image.url
        return data


class IngredientForPostSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredients_Amount
        fields = ('id', 'amount')


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор при создании рецепта, модели Recipe."""

    ingredients = IngredientForPostSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    @staticmethod
    def create_ingredients(recipe, ingredients):
        for ingredient in ingredients:
            Ingredients_Amount.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )

    @staticmethod
    def create_tags(recipe, tags):
        for tag in tags:
            recipe.tags.add(tag)

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        tags = self.initial_data.get('tags')
        tags_list = []
        if not ingredients:
            raise ValidationError('Не выбраны ингредиенты')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise ValidationError(
                    f'{ingredient} указано не допустимое кол-во ингредиентов :'
                )
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться'
                )
            ingredients_list.append(ingredient['id'])
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Теги не должны повторяться'
                )
            tags_list.append(tag)
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )
        self.create_tags(recipe, tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        Ingredients_Amount.objects.filter(recipe=recipe).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.create_tags(recipe, tags)
        self.create_ingredients(recipe, ingredients)
        return super().update(recipe, validated_data)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['image'] = obj.image.url
        return data


class FavoritesSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов, модели Favorites."""

    class Meta:
        model = Favorites
        fields = ('user', 'recipe')

    def validate(self, data):
        if Favorites.objects.filter(
                user=self.context['request'].user,
                recipe=data['recipe']
        ):
            raise serializers.ValidationError(
                'Вы уже добавили этот рецепт в избранное.'
            )
        return data

    def to_representation(self, instance):
        return FavoritesViewSerilizer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class FavoritesViewSerilizer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов в корзине, модели ShoppingCart."""
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        if ShoppingCart.objects.filter(
                user=self.context['request'].user,
                recipe=data['recipe']
        ):
            raise serializers.ValidationError(
                'Вы уже добавили этот рецепт в список покупок.'
            )
        return data

    def to_representation(self, instance):
        return FavoritesViewSerilizer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
