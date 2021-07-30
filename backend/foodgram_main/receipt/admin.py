from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag, Follow)

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(ShoppingCart)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
admin.site.register(Follow)
