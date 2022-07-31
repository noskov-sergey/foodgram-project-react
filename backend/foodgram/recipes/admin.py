from django.contrib import admin

from .models import ShopingCart, Tag, Ingredient, Recipe, IngredientsAmount, Favorites

class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
    )
    search_fields = (
        'name',
        'author',
        'tags',
    )

class Ingredients_amountAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = (
        'id',
    )


@admin.register(Favorites)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )

@admin.register(ShopingCart)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )

admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientsAmount, Ingredients_amountAdmin)