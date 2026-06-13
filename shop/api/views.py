from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny 
from rest_framework.views import APIView
from api.filters import ProductFilter, InstockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


#function based views
# @api_view(['GET']) #this decorator limits to GET requests #this makes it so you can view the browsable api
# def product_list(request):
#     products = Product.objects.all() #ORM query
#     serializer = ProductSerializer(products, many=True) #for querysets you need many=True
#     return Response(serializer.data)
# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,  #need to have this because filter_backends overrides filter defined in settings
        filters.SearchFilter, 
        filters.OrderingFilter,
        InstockFilterBackend,   #this will auto filterout all stocks <= 0
    ]
    search_fields = ['=name', 'description'] #=name means exact match in name
    ordering_fields = ['name', 'price', 'stock']

    def get_permissions(self):
        self.permission_classes = [AllowAny] #allow any to use endpoint
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# @api_view(['GET'])
# def product_detail(request, pk):
#     products = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(products) #converts to json
#     return Response(serializer.data)
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id' #this sets what url argument we use when looking up value in urls.py. Default is 'fk'.

    def get_permissions(self):
        self.permission_classes = [AllowAny] #allow anyone to use endpoint
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

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

#this displays all orders made by a specific user
class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): #from GenericAPIView (superclass of ListAPIView)
        qs = super().get_queryset() #this gets the base queryset from the super ListAPIView
        return qs.filter(user=self.request.user) #filter for user that is authenticated
        #request is there in class based view get_queryset method

#function based view
# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({ #this passes a dictionary to create a temporary object-like dictionary with these fields
#         'products': products,            #since these fields are not part of a model
#         'count': len(products),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price'] #I don't need to learn how aggregate works for now
#     })
#     return Response( serializer.data)
class ProdcutInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({ #this passes a dictionary to create a temporary object-like dictionary with these fields
            'products': products,            #since these fields are not part of a model
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'] #I don't need to learn how aggregate works for now
        })
        return Response(serializer.data)