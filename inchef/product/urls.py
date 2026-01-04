from django.urls import path
from .views import products, product_detail, create_product

urlpatterns = [
    path('', products, name='products'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('create/', create_product, name='create_product')
]
