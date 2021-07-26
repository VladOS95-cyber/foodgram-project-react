from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=200, blank=False)
    color = models.CharField(max_length=200, blank=False, null=True)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=False,
        null=True
    )


class Ingredient(models.Model):
    name = models.CharField(max_length=200, blank=False)
    measurement_unit = models.CharField(max_length=200, blank=False)


class RecipeIngredient(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        blank=False)
    amount = models.PositiveIntegerField(blank=False)


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='tags')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=False
    )
    image = models.CharField(max_length=500)
    ingredients = models.ManyToManyField(
        RecipeIngredient)
    is_favorited = models.BooleanField(blank=False, default=False)
    is_in_shopping_cart = models.BooleanField(blank=False, default=False)
    name = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=500, blank=False)
    cooking_time = models.PositiveIntegerField(blank=False)


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='purchases', verbose_name='Пользователь')
    purchase = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='customers', verbose_name='Покупка')


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    wish = models.ForeignKey(
        Recipe, on_delete=models.CASCADE)
