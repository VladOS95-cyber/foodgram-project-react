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


class Ingredients(models.Model):
    name = models.CharField(max_length=200, blank=False)
    measurement_unit = models.CharField(max_length=200, blank=False)
    amount = models.PositiveIntegerField()


class ReceiptDetailed(models.Model):
    tags = models.ManyToManyField(Tag, related_name='tags')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=False
    )
    ingredients = models.ManyToManyField(Ingredients, related_name='receipt')
    is_favorited = models.BooleanField(blank=False)
    is_in_shopping_cart = models.BooleanField(blank=False)
    name = models.CharField(max_length=200, blank=False)
    image = models.URLField(blank=False)
    text = models.TextField(max_length=500, blank=False)
    cooking_time = models.PositiveIntegerField()
