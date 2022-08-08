from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save

from users.models import FoodgramUser


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField(
        'название ингредиента',
        db_index=True,
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


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='автор публикации',
    )
    name = models.CharField(
        'название',
        max_length=200,
    )
    image = models.ImageField(
        'картинка',
        upload_to='recipes/',
    )
    text = models.TextField(
        'описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Ingredients_Amount',
        related_name='ingredients',
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


class Ingredients_Amount(models.Model):
    """Допольнительная модель для учета количества ингидиентов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'количество',
    )

    class Meta:
        verbose_name = 'Количественные связи'
        verbose_name_plural = 'Количественные связи'
        constraints = (
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient'
            ),
        )
    
    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'


class Favorites(models.Model):
    """Модель добавленных в избранное рецептов."""

    user = models.ForeignKey(
        FoodgramUser,
        related_name='favorited',
        verbose_name='добавил в избранное',
        on_delete=models.CASCADE,
        help_text='добавил в избранное',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorited',
        verbose_name='понравился рецепт',
        on_delete=models.CASCADE,
        help_text='понравился рецепт',
    )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favoritesRecipe'
            ),
        )


class ShoppingCart(models.Model):
    """Модель добавленных в лист покупок рецептов."""

    user = models.ForeignKey(
        FoodgramUser,
        related_name='shopping_cart',
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        help_text='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
        verbose_name='доавбленный в корзину рецепт',
        on_delete=models.CASCADE,
        help_text='доавбленный в корзину рецепт',
    )

    class Meta:
        verbose_name = 'добавбленный в корзину рецепт'
        verbose_name_plural = 'добавбленные в корзину рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='shoppingart'
            ),
        )
