from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()), #we need to use as_view() for class based views
    path('products/info/', views.ProdcutInfoAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
]

router = DefaultRouter() #creates the router object which generates the ViewSet routes
router.register('orders', views.OrderViewSet) #sets the prefix and which ViewSet to attach to
urlpatterns += router.urls #this adds all the router routes to urlpatterns