from django.db import models

from users.models import User


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
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
        through='Ingredients_amount',
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

    class Meta:
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
        'название',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'единицы измерения',
        max_length=200,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    def __str__(self) -> str:
        return self.name


class Ingredients_amount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
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

    def __str__(self) -> str:
        return self.recipe.name