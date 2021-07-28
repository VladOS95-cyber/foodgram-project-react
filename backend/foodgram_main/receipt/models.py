from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='tag_name')
    color = models.CharField(
        max_length=200,
        null=True,
        verbose_name='tag_color'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='tag_slug'
    )

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='ingredient_name')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='ingredient_measure'
    )

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, verbose_name='tags')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='author'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ingredients')
    image = models.CharField(max_length=500, verbose_name='image')
    name = models.CharField(max_length=200, verbose_name='name')
    text = models.TextField(max_length=500, verbose_name='description')
    cooking_time = models.PositiveIntegerField(verbose_name='cooking_time')

    class Meta:
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE, verbose_name='ingredients')
    amount = models.PositiveIntegerField(verbose_name='quantity')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='recipe')

    class Meta:
        verbose_name = 'ingredients_for_recipe'
        verbose_name_plural = 'ingredients_for_recipes'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='users', verbose_name='user')
    purchase = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='purchase')

    class Meta:
        verbose_name = 'shopping_cart'
        verbose_name_plural = 'shopping_carts'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='user')
    wish = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='favorite')

    class Meta:
        verbose_name = 'favorite_list'
        verbose_name_plural = 'favorite_lists'
