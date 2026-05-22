from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()), #we need to use as_view() for class based views
    path('products/info/', views.product_info),
    path('products/<int:product_id>/', views.ProductListAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),
]