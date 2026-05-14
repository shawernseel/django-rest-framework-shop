from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta: #we use this for ModelSerializer
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock',
        )

    def validate_price(self, value): #drf has field level validation for validate_<field name>
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'product', #fk
            'quantity',
        )
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) #serializes OrderItem objects in Order when serializing Order

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',         #note how user is a fk
            'status',
            'items',
        )