from api.filters import InstockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, OrderItem, Product
from api.pagination import (ProductLimitOffsetPagination,
                            ProductPageNumberPagination)
from api.serializers import (OrderSerializer, ProductInfoSerializer,
                             ProductSerializer, OrderCreateSerializer)
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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
    queryset = Product.objects.order_by('pk')
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
    #pagination_class = ProductPageNumberPagination
    pagination_class = ProductLimitOffsetPagination

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

#1st rendition
# @api_view(['GET'])
# def order_list(request):
#     #orders = Order.objects.all() #bellow is an optomization for this line
#     orders = Order.objects.prefetch_related(
#         #'items' #this is commented out because the below will include this implicitly
#         'items__product' #uses related name to prefetch
#     ) #.all() #prefetch_related automatically includes .all() so we don't need a .all() here
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

#2nd rendition
# class OrderListAPIView(generics.RetrieveAPIView):
#     products = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer

#this displays all orders made by a specific user
# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self): #from GenericAPIView (superclass of ListAPIView)
#         qs = super().get_queryset() #this gets the base queryset from the super ListAPIView
#         return qs.filter(user=self.request.user) #filter for user that is authenticated
#         #request is there in class based view get_queryset method

#3rd rendition, users can still see all users' orders via the /orders endpoint (even though /orders/user-orders limits it)
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = None
#     filterset_class = OrderFilter
#     filter_backends = [DjangoFilterBackend]

#     @action(
#         detail=False, #detail=False for single object; detail=True for list of objects
#         methods=['get'],
#         url_path='user-orders', # GET /orders/user_orders/ is the router generated route. Now it is GET /orders/user-orders/
#         #permission_classes=[IsAuthenticated] #can add permissions for just this action
#     )
#     def user_orders(self, request):
#         orders = self.get_queryset().filter(user=request.user)
#         serializer = self.get_serializer(orders, many=True)
#         return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # overriding special method that let's you dynamically pick the serializer class
    def get_serializer_class(self):  # pyright: ignore[reportIncompatibleMethodOverride]
        # can also check if POST: if self.request.method == 'POST'<<
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()

    # overriding special method for dynamic query filtering
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user) #limiting visible orders to users' orders if user is not staff
        return qs


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