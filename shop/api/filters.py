import django_filters
from api.models import Order, Product
from rest_framework import filters


#Pure DRF filtering
class InstockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

#django-filter filtering
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], #i just means case insensitive
            'price': ['exact', 'lt', 'gt', 'range']
        }

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date') #uses django_filters DateFilter so that it works by day not minutes/secs
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['exact', 'lt', 'gt']
        }