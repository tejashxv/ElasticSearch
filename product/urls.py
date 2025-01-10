from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductsAPI.as_view(), name='products'),
    path('product/<id>/', views.ProductDetailAPI.as_view(), name='product_detail'),
    path('', views.shop, name='shop'),
    path('products/<id>', views.product_detail, name='shop'),
]