# Generated by Django 3.2.5 on 2021-07-26 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0004_receiptdetailed_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredients',
            new_name='Ingredient',
        ),
    ]
