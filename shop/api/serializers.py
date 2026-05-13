from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta: #we use this for ModelSerializer
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'stock',
        )

    def validate_price(self, value): #drf has field level validation for validate_<field name>
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value