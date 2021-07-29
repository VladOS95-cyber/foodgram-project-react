from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import CustomUser, Follow

from .format_transition import Hex2NameColor
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class UserDetailSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        'get_is_subscribed')

    def get_is_subscribed(self, obj):
        current_user = obj
        request = self.context.get('request')
        if request:
            current_user = request.user
        if current_user.is_anonymous:
            return False
        return (current_user == obj) or Follow.objects.filter(
            user=current_user, following=obj
        ).exists()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='following.id')
    email = serializers.ReadOnlyField(source='following.email')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')
    recipes = serializers.SerializerMethodField('get_recipe')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    def get_recipe(self, obj):
        author = obj.following
        recipes = Recipe.objects.filter(author=author)
        return ReceiptDetailedSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        author = obj.following
        count = Recipe.objects.filter(author=author).count()
        return count

    def get_is_subscribed(self, obj):
        author = obj.following
        user = obj.user
        return Follow.objects.filter(following=author, user=user).exists()

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsForRecipe(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ReceiptDetailedSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField('get_ingredients')
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart'
    )

    def get_ingredients(self, obj):
        qs = RecipeIngredient.objects.filter(recipe=obj)
        return IngredientsForRecipe(qs, many=True).data

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(wish=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(purchase=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class ShoppingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='purchase.id')
    name = serializers.ReadOnlyField(source='purchase.name')
    image = serializers.ReadOnlyField(source='purchase.image')
    cooking_time = serializers.ReadOnlyField(source='purchase.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FavorSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='wish.id')
    name = serializers.ReadOnlyField(source='wish.name')
    image = serializers.ReadOnlyField(source='wish.image')
    cooking_time = serializers.ReadOnlyField(source='wish.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
