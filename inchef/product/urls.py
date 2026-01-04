from django.urls import path
from .views import products, product_detail, create_product, edit_product


urlpatterns = [
    path('', products, name='products'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('<int:pk>/edit/', edit_product, name='edit_product'),
    path('create/', create_product, name='create_product')
]