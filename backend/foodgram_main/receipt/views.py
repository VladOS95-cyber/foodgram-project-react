from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .all_serializers import (FavorSerializer, IngredientsSerializer,
                              ReceiptDetailedSerializer, ShoppingSerializer,
                              TagSerializer)
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .filters import RecipeFilter


class MixinTransition(
    ListModelMixin,
        RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    serializer_class = ReceiptDetailedSerializer
    filter_class = RecipeFilter


class TagsViewSet(MixinTransition):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientsViewSet(MixinTransition):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', ]


class AddToShoping(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if ShoppingCart.objects.filter(user=user, purchase=recipe).exists():
            return Response(
                'Рецепт уже добавлен в карту покупок',
                status=status.HTTP_400_BAD_REQUEST)
        purchase = ShoppingCart.objects.create(user=user, purchase=recipe)
        serializer = ShoppingSerializer(purchase)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        shopping = get_object_or_404(ShoppingCart, user=user, id=id)
        shopping.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class AddToFavorite(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if Favorite.objects.filter(user=user, wish=recipe).exists():
            return Response(
                'Рецепт уже добавлен в избранное',
                status=status.HTTP_400_BAD_REQUEST)
        favor = Favorite.objects.create(user=user, wish=recipe)
        serializer = FavorSerializer(favor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        favorite = get_object_or_404(Favorite, user=user, id=id)
        favorite.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def get(self, request):
        user = request.user
        recipes = Recipe.objects.filter(shoppingcart__user=user)
        ingredients = []
        for recipe in recipes:
            ingredients.append(recipe.ingredients.all())
        new_ingredients = []
        for ingredients_set in ingredients:
            for ingredient in ingredients_set:
                new_ingredients.append(ingredient)
        ingredients_dict = {}
        for ing in new_ingredients:
            if ing in ingredients_dict:
                ingredients_dict[ing] += ing.amount
            else:
                ingredients_dict[ing] = ing.amount
        wishlist = []
        for recipe_ing, quantity in ingredients_dict.items():
            wishlist.append(
                f'{recipe_ing.ingredient.name} - {quantity} {recipe_ing.ingredient.measurement_unit} \n')
        wishlist.append('\n')
        wishlist.append('FoodGram, 2021')
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response
