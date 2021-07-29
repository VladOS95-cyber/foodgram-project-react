# Generated by Django 3.2.5 on 2021-07-29 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='название ингредиента')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='ед. измерения')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=500, verbose_name='картинка')),
                ('name', models.CharField(max_length=200, verbose_name='название')),
                ('text', models.TextField(max_length=500, verbose_name='описание')),
                ('cooking_time', models.PositiveIntegerField(verbose_name='время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='название тэга')),
                ('color', models.CharField(max_length=200, null=True, verbose_name='цвет тэга')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='слаг')),
            ],
            options={
                'verbose_name': 'тэг',
                'verbose_name_plural': 'тэги',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipt.recipe', verbose_name='покупка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'карта покупок',
                'verbose_name_plural': 'карты покупок',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipt.ingredient', verbose_name='ингредиент')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='receipt.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'ингредиенты для рецепта',
                'verbose_name_plural': 'ингредиенты для рецептов',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, through='receipt.RecipeIngredient', to='receipt.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='receipt.Tag', verbose_name='тэги'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
                ('wish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipt.recipe', verbose_name='избранное')),
            ],
            options={
                'verbose_name': 'список избранного',
                'verbose_name_plural': 'списки избранного',
            },
        ),
    ]
