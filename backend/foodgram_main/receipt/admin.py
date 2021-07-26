from django.contrib import admin
from .models import Tag, Ingredient, Recipe, ShoppingCart, RecipeIngredient, Favorite

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(ShoppingCart)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
