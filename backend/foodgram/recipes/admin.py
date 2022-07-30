from django.contrib import admin

from .models import Tag, Ingredient, Recipe, Ingredients_amount

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

admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients_amount, Ingredients_amountAdmin)