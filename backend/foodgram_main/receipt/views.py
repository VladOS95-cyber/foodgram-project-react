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


class MixinTransition(
    ListModelMixin,
        RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ReceiptDetailedSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'name', 'tags']


class TagsViewSet(MixinTransition):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


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
        purchase = ShoppingCart.objects.create(user=user, purchase=recipe)
        serializer = ShoppingSerializer(purchase)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        shopping = ShoppingCart.objects.get(user=user, id=id)
        shopping.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class AddToFavorite(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        favor = Favorite.objects.create(user=user, wish=recipe)
        serializer = FavorSerializer(favor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        favorite = Favorite.objects.get(user=user, id=id)
        favorite.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        users_shopping_list_recipes = user.purchases.all()
        recipes = []
        for i in users_shopping_list_recipes:
            recipes.append(i.purchase)
        ingredients = []
        for recipe in recipes:
            ingredients.append(recipe.ingredients.all())
        new_ingredients = []
        for set in ingredients:
            for ingredient in set:
                new_ingredients.append(ingredient)
        ingredients_dict = {}
        for ing in new_ingredients:
            if ing in ingredients_dict.keys():
                ingredients_dict[ing] += ing.quantity
            else:
                ingredients_dict[ing] = ing.quantity
        wishlist = []
        for k, v in ingredients_dict.items():
            wishlist.append(f'{k.name} - {v} {k.unit} \n')
        wishlist.append('\n')
        wishlist.append('FoodGram, 2021')
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response
