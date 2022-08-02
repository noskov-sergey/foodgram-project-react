from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save

from users.models import FoodgramUser


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор публикации',
    )
    name = models.CharField(
        'название',
        max_length=200,
    )
    image = models.ImageField(
        'картинка',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        'описание',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientsAmount',
        through_fields=('recipe', 'ingredient'),
        verbose_name='ингредиенты',
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='тэг',
    )
    cooking_time = models.IntegerField(
        'время приготовления в минутах',
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created',]
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return self.name

    def get_ingredients(self):
        return ", ".join([str(ingredient) for ingredient in self.ingredients.all()])
    
    def get_tags(self):
        return ", ".join([str(tag) for tag in self.tags.all()])


class Tag(models.Model):
    """Модель тэга."""

    name = models.CharField(
        'название',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        'цветовой HEX-код',
        max_length=7,
        unique=True,
        null=True,
    )
    slug = models.SlugField(
        'уникальный слаг',
        max_length=150,
        unique=True,
        null=True,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField(
        'название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=200,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    def __str__(self) -> str:
        return self.name


class IngredientsAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="related_ingredients",
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        'количество',
    )

    class Meta:
        verbose_name = 'Количественные связи'
        verbose_name_plural = 'Количественные связи'
        unique_together = (
            ('recipe', 'ingredient'),
        )

    def __str__(self) -> str:
        return self.recipe.name


class Favorites(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        related_name='elector',
        verbose_name='добавил в избранное',
        on_delete=models.CASCADE,
        help_text='добавил в избранное',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        verbose_name='понравился рецепт',
        on_delete=models.CASCADE,
        help_text='понравился рецепт',
    )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'
        unique_together = (
            ('user', 'recipe'),
        )


class ShopingCart(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        related_name='costumer',
        verbose_name='покупатель',
        on_delete=models.CASCADE,
        help_text='покупатель',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shoping_cart',
        verbose_name='доавбленный в корзину рецепт',
        on_delete=models.CASCADE,
        help_text='доавбленный в корзину рецепт',
    )

    class Meta:
        verbose_name = 'доавбленный в корзину рецепт'
        verbose_name_plural = 'доавбленныу в корзину рецепты'
        unique_together = (
            ('user', 'recipe'),
        )
