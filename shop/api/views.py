from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

#function based views
# @api_view(['GET']) #this decorator limits to GET requests #this makes it so you can view the browsable api
# def product_list(request):
#     products = Product.objects.all() #ORM query
#     serializer = ProductSerializer(products, many=True) #for querysets you need many=True
#     return Response(serializer.data)
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0) #this will filter out stocks <= 0
    serializer_class = ProductSerializer

# @api_view(['GET'])
# def product_detail(request, pk):
#     products = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(products) #converts to json
#     return Response(serializer.data)
class ProductDetailAPIView(generics.RetrieveAPIView):
    products = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id' #this sets what url argument we use when looking up value in urls.py. Default is 'fk'.

# @api_view(['GET'])
# def order_list(request):
#     #orders = Order.objects.all() #bellow is an optomization for this line
#     orders = Order.objects.prefetch_related(
#         #'items' #this is commented out because the below will include this implicitly
#         'items__product' #uses related name to prefetch
#     ) #.all() #prefetch_related automatically includes .all() so we don't need a .all() here
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)
class OrderListAPIView(generics.RetrieveAPIView):
    products = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({ #this passes a dictionary to create a temporary object-like dictionary with these fields
        'products': products,            #since these fields are not part of a model
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price'] #I don't need to learn how aggregate works for now
    })
    return Response(serializer.data)