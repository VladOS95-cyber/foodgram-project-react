from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='название тэга')
    color = models.CharField(
        max_length=200,
        null=True,
        verbose_name='цвет тэга'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='слаг'
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='название ингредиента')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='ед. измерения'
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, verbose_name='тэги')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=True,
        through='RecipeIngredient', 
        verbose_name='ингредиенты')
    image = models.CharField(max_length=500, verbose_name='картинка')
    name = models.CharField(max_length=200, verbose_name='название')
    text = models.TextField(max_length=500, verbose_name='описание')
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления')

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент')
    amount = models.PositiveIntegerField(verbose_name='количество')

    class Meta:
        verbose_name = 'ингредиенты для рецепта'
        verbose_name_plural = 'ингредиенты для рецептов'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name='пользователь')
    purchase = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='покупка')

    class Meta:
        verbose_name = 'карта покупок'
        verbose_name_plural = 'карты покупок'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    wish = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='избранное')

    class Meta:
        verbose_name = 'список избранного'
        verbose_name_plural = 'списки избранного'
