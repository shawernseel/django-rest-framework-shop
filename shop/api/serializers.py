from django.db import transaction 
from rest_framework import serializers
from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta: #we use this for ModelSerializer
        model = Product
        fields = (
            'id', #it's nice to have id in the endpoint
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

class OrderCreateSerializer(serializers.ModelSerializer):
    #serializes nested "items" data, it will serialize each one because of the many=True
    class OrderItemCreateSerializer(serializers.ModelSerializer): #we can also define this outside, it's here because it is used nowhere else
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items', #this is the fk related name from OrderItem since we are accessing it from the reverse side
        )
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        # validated_data is the cleaned version of the request body.
        # DRF has already checked that the data is valid and converted IDs into actual model objects, for example:
        # Request data:
        # {"user": 2, "status": "Pending", "items": [{"product": 27, "quantity": 2},{"product": 28, "quantity": 2}]}
        #
        # validated_data:
        # {"user": <User: john-doe>, "status": "Pending",
        #  "items": [{"product": <Product: Velvet Underground & Nico>, "quantity": 2}, {'product': <Product 28 Object>, 'quantity': 1}]
        orderitem_data = validated_data.pop('items')

        with transaction.atomic(): #if any part fails it will roll back ro avoid partial changes
            order = Order.objects.create(**validated_data) #is equivalent to below
            #order = Order.objects.create(user=validated_data["user"],status=validated_data["status"])

            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)
                #order = <Order: Order 61f95f59-2dfc-4dbf-9c0f-5177b1d730cd by john-doe>
                #item = {'product': <Product: Velvet Underground & Nico>, 'quantity': 2}
        return order
    
    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            #update user and status, DRF can serialize non nested data by default
            instance = super().update(instance, validated_data)

            if orderitem_data is not None:
                # Clear existing items (optional, depends on requirements)
                instance.items.all().delete()

                #Recreate items with the updated data
                for item in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)

        return instance

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