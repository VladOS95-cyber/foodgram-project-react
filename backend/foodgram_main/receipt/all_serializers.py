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
        request = self.context.get('request', None)
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
    id = serializers.SerializerMethodField('get_id')
    email = serializers.SerializerMethodField('get_email')
    username = serializers.SerializerMethodField('get_username')
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')
    recipes = serializers.SerializerMethodField('get_recipe')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    def get_id(self, obj):
        author = obj.following
        return author.id

    def get_email(self, obj):
        author = obj.following
        return author.email

    def get_username(self, obj):
        author = obj.following
        return author.username

    def get_first_name(self, obj):
        author = obj.following
        return author.first_name

    def get_last_name(self, obj):
        author = obj.following
        return author.last_name

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
    id = serializers.SerializerMethodField('get_id')
    name = serializers.SerializerMethodField('get_name')
    measurement_unit = serializers.SerializerMethodField(
        'get_measurement_unit')

    def get_id(self, obj):
        ingredient = obj.ingredients
        return ingredient.id

    def get_name(self, obj):
        ingredient = obj.ingredients
        return ingredient.name

    def get_measurement_unit(self, obj):
        ingredient = obj.ingredients
        return ingredient.measurement_unit

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class ReceiptDetailedSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    ingredients = IngredientsForRecipe(many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart'
    )

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
    id = serializers.SerializerMethodField('get_id')
    name = serializers.SerializerMethodField('get_name')
    image = serializers.SerializerMethodField('get_image')
    cooking_time = serializers.SerializerMethodField('get_cooking_time')

    def get_id(self, obj):
        receipe = obj.purchase
        return receipe.id

    def get_name(self, obj):
        receipe = obj.purchase
        return receipe.name

    def get_image(self, obj):
        receipe = obj.purchase
        return receipe.image

    def get_cooking_time(self, obj):
        receipe = obj.purchase
        return receipe.cooking_time

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FavorSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id')
    name = serializers.SerializerMethodField('get_name')
    image = serializers.SerializerMethodField('get_image')
    cooking_time = serializers.SerializerMethodField('get_cooking_time')

    def get_id(self, obj):
        receipe = obj.wish
        return receipe.id

    def get_name(self, obj):
        receipe = obj.wish
        return receipe.name

    def get_image(self, obj):
        receipe = obj.wish
        return receipe.image

    def get_cooking_time(self, obj):
        receipe = obj.wish
        return receipe.cooking_time

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
