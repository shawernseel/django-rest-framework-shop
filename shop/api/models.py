from django.db import models
from django.contrib.auth.models import AbstractUser


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
        