from django.http import JsonResponse
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view

#function based views
@api_view(['GET']) #this decorator limits to GET requests #this makes it so you can view the browsable api
def product_list(request):
    products = Product.objects.all() #ORM query
    serializer = ProductSerializer(products, many=True) #for querysets you need many=True
    return Response(serializer.data)