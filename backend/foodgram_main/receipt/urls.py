from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AddToFavorite, AddToShoping, DownloadShoppingCart,
                    IngredientsViewSet, ReceiptViewSet, TagsViewSet)
from users.views import SubscribeView, ShowSubscriptionsView

router_v1 = DefaultRouter()

router_v1.register('recipes', ReceiptViewSet, basename='Recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='Ingredients')
router_v1.register('tags', TagsViewSet, basename='Tags')


urlpatterns = [
    path(
        'users/<int:author_id>/subscribe/',
        SubscribeView.as_view(),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        ShowSubscriptionsView.as_view(),
        name='subscriptions'
    ),
    path(
        'recipes/<int:recipe_id>/favorite/',
        AddToFavorite.as_view(),
        name='favorite'),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        AddToShoping.as_view(),
        name='shopping_cart'),
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCart.as_view(),
        name='get_shopping_cart'
    ),
    path('', include(router_v1.urls))
]