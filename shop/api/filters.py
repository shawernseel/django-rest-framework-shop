import django_filters
from api.models import Product
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
