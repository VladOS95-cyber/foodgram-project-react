from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AddToFavorite, AddToShoping, DownloadShoppingCart,
                    IngredientsViewSet, ReceiptViewSet, TagsViewSet)

router_v1 = DefaultRouter()

router_v1.register('recipes', ReceiptViewSet, basename='Recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='Ingredients')
router_v1.register('tags', TagsViewSet, basename='Tags')


urlpatterns = [
    path(
        r'recipes/<int:id>/favorite/',
        AddToFavorite.as_view(),
        name='favorite'),
    path(
        r'recipes/<int:id>/shopping_cart/',
        AddToShoping.as_view(),
        name='shopping_cart'),
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCart.as_view(),
        name='get_shopping_cart'
    ),
    path('', include(router_v1.urls))
]