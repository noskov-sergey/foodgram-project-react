from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from recipes.models import Tag, Ingredient, Recipe, IngredientsAmount, Favorites, ShopingCart
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов, модели Tag."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов, модели Tag."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            #'' ,
        )


class IngredientDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = ReadOnlyField(source='ingredient.id')    
    ingredient = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'ingredient', 'measurement_unit', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта, модели Recipe."""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientDetailSerializer(source="related_ingredients", many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(recipe=obj, user=request.user).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShopingCart.objects.filter(recipe=obj, user=request.user).exists()