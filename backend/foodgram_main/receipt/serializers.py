from rest_framework import serializers
from .models import Tag, Ingredients, ReceiptDetailed


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ReceiptDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptDetailed
        fields = '__all__'
