from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
