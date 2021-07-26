# Generated by Django 3.2.5 on 2021-07-26 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0007_auto_20210726_1428'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='receipt', to='receipt.RecipeIngredient'),
        ),
    ]
