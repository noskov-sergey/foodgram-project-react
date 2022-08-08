from django.contrib import admin

from .models import (Ingredients_Amount, Favorites, Ingredient,
                     Recipe, ShoppingCart, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    empty_value_display = '-пусто-'


class AmountIngredientForRecipeInLine(admin.TabularInline):
    model = Ingredients_Amount


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    readonly_fields = ('number_additions_to_favorites',)
    list_filter = ('author', 'name', 'tags')
    list_per_page = 20
    inlines = [AmountIngredientForRecipeInLine]
    empty_value_display = '-пусто-'

    def number_additions_to_favorites(self, obj):
        return obj.favorite.count()


@admin.register(Ingredients_Amount)
class AmountIngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe', 'ingredient', 'amount'
    )
    list_filter = ('recipe', 'ingredient')
    empty_value_display = '-пусто-'


@admin.register(Favorites)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'