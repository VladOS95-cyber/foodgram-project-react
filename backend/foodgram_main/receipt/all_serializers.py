from .fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag, ReceiptTag, Follow)
from django.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class ShowRecipeAddedSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = fields

    def get_image(self, obj):
        request = self.context.get('request')
        photo_url = obj.image.url
        return request.build_absolute_uri(photo_url)


class UserDetailSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(
        label=('Password',),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Неверные учетные данные.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Запрос должен содержать email и пароль.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsForRecipe(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_ingredients(self, obj):
        qs = RecipeIngredient.objects.filter(recipe=obj)
        return IngredientsForRecipe(qs, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj,
                                       user=request.user).exists()

    def get_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount'
        )


class ShowRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserDetailSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField('get_ingredients')
    is_in_shopping_cart = serializers.SerializerMethodField('get_is_in_shopping_cart')
    is_favorited = serializers.SerializerMethodField('get_is_favorited')

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

    def get_ingredients(self, obj):
        record = RecipeIngredient.objects.filter(recipe=obj)
        return IngredientsForRecipe(record, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        user = request.user
        return Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        user = request.user
        return ShoppingCart.objects.filter(recipe=obj, user=user).exists()


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=300,
        use_url=True
    )
    author = UserDetailSerializer(read_only=True)
    ingredients = AddIngredientToRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        for item in ingredients:
            if int(item['amount']) < 0:
                raise serializers.ValidationError(
                    {'ingredients': (
                        'Убедитесь, что значение количества ингредиента больше 0')
                    }
                )
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                'Введите целое число больше 0 для времени готовки'
            )
        return data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient in ingredients_data:
            ingredient_model = ingredient['id']
            amount = ingredient['amount']
            RecipeIngredient.objects.create(
                ingredient=ingredient_model,
                recipe=recipe,
                amount=amount
            )
        for tag in tags_data:
            ReceiptTag.objects.create(recipe=recipe, tag=tag)
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        ingredient_data = validated_data.pop('ingredients')
        ReceiptTag.objects.filter(recipe=instance).delete()
        for tag in tags_data:
            ReceiptTag.objects.create(
                recipe=instance,
                tag=tag
            )
        RecipeIngredient.objects.filter(recipe=instance).delete()
        for new_ingredient in ingredient_data:
            RecipeIngredient.objects.create(
                ingredient=new_ingredient['id'],
                recipe=instance,
                amount=new_ingredient['amount']
            )
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        data = ShowRecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


class FavorSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        user = self.context.get('request').user
        recipe_id = data['recipe'].id

        if (self.context.get('request').method == 'GET'
                and Favorite.objects.filter(user=user,
                                            recipe__id=recipe_id).exists()):
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное')

        recipe = get_object_or_404(Recipe, id=recipe_id)

        if (self.context.get('request').method == 'DELETE'
                and not Favorite.objects.filter(
                    user=user,
                    recipe=recipe).exists()):
            raise serializers.ValidationError()

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowRecipeAddedSerializer(
            instance.recipe,
            context=context).data


class ShoppingSerializer(serializers.ModelSerializer):
    class Meta(FavorSerializer.Meta):
        model = ShoppingCart

    def validate(self, data):
        user = self.context.get('request').user
        recipe_id = data['recipe'].id
        if (self.context.get('request').method == 'GET'
                and ShoppingCart.objects.filter(
                    user=user,
                    recipe__id=recipe_id
                ).exists()):
            raise serializers.ValidationError(
                'Продукты уже в корзине')

        recipe = get_object_or_404(Recipe, id=recipe_id)

        if (self.context.get('request').method == 'DELETE'
                and not ShoppingCart.objects.filter(
                    user=user,
                    recipe=recipe).exists()):
            raise serializers.ValidationError()

        return data


class ShowFollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count')
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.follower.filter(user=obj, author=request.user).exists()

    def get_recipes(self, obj):
        recipes = obj.recipes.all()[:settings.RECIPES_LIMIT]
        request = self.context.get('request')
        context = {'request': request}
        return ShowRecipeAddedSerializer(
            recipes,
            many=True,
            context=context).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FollowSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    author = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Follow
        fields = (
            'user',
            'author'
        )

    def validate(self, data):
        user = self.context.get('request').user
        author_id = data['author'].id
        follow_exist = Follow.objects.filter(
            user=user,
            author__id=author_id
        ).exists()

        if self.context.get('request').method == 'GET':
            if user.id == author_id or follow_exist:
                raise serializers.ValidationError(
                    'Подписка существует')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowFollowSerializer(
            instance.author,
            context=context).data
