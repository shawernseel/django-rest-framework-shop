from api.models import Order, OrderItem, User
from django.contrib import admin


# Register your models here.
class OrderItemInline(admin.TabularInline): #attaches related objects to order when creating the order from admin
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline #uses the class above so that OrderAdmin which extends ModelAdmin can edit Models
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(User)