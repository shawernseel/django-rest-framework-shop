import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

#need to add AUTH_USER_MODEL in settings.py
class User(AbstractUser): #Abstracts Django's default User model
    pass

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField() #as many characters as you want
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField() #how much product is in stock
    image = models.ImageField(upload_to='products/', blank=True, null=True) #will store product images under products/

    @property #getter
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self): #shows naming for printed objects
        return self.name
    
class Order(models.Model):
    class StatusChoices(models.TextChoices): #like an enum
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'
    
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField( #stores text shows status of order in its lifecycle
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING       
    )

    products = models.ManyToManyField(Product, through="OrderItem", related_name='orders') 
    #related_name defines access from the other side ex. prodect.orders.all()

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

#this is a through model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"