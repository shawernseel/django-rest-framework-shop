from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta: #we use this for ModelSerializer
        model = Product
        fields = (
            'description',
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
    #product = ProductSerializer() #this is what we would do if we wanted data unflattened wrapped in { product }

    #product_name and product_price are flattened from product (displayed at same level as quantity and other fields in OrderItem)
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price'
    )
    
    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal', #@property getters can just go in here too!
        )

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True) #makes it so that when creating an Order we don't need to input the ID its generated here
    items = OrderItemSerializer(many=True, read_only=True) #serializes OrderItem objects in Order when serializing Order
    total_price = serializers.SerializerMethodField() #by default this is serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, obj):
        order_items = obj.items.all() #item is the related name
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',         #note how user is a fk
            'status',
            'items',        #this is the fk related name from OrderItem since we are accessing it from the reverse side
            'total_price'
        )

#use a genaric serializer when the data is not tied to a particular model
class ProductInfoSerializer(serializers.Serializer):
    #get all products count of products, max price
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()