from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    availability_message = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',
            'category', 'stock', 'is_available',
            'availability_message',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['is_available', 'availability_message']

    def get_availability_message(self, obj):
        return obj.availability_message
