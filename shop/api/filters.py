import django_filters
from api.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], #i just means case insensitive
            'price': ['exact', 'lt', 'gt', 'range']
        }
