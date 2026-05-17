from django.core.management.base import BaseCommand
from api.models import User, Product, Order, OrderItem


class Command(BaseCommand):
    help = "Delete dummy data created by populate_db"

    def handle(self, *args, **kwargs):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()

        # optional: delete admin user created by populate_db
        # User.objects.filter(username="admin").delete()

        self.stdout.write(
            self.style.SUCCESS("Deleted OrderItems, Orders, and Products.")
        )