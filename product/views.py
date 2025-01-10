from django.shortcuts import render
from .models import product
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from .productRecommender import get_similer_products
# Create your views here.
class ProductsAPI(APIView):
    def get(self, request):
        _product = product.objects.all().order_by('?')[:40]
        serializer = ProductSerializer(_product, many=True)
        return Response({'products': serializer.data})

class ProductDetailAPI(APIView):
    def get(self, request, id):
        _product = product.objects.get(id = id)
        serializer = ProductSerializer(_product)
        similar_product = get_similer_products(id ,20)
        similar_product_serializer = ProductSerializer(similar_product, many=True)
        return Response({'product': serializer.data, 'similar_products': similar_product_serializer.data})
    
def shop(request):
    _product = product.objects.all().order_by('?')[:40]
    return render(request, 'home.html', {'product': _product})
    
def product_detail(request, id):
    _product = product.objects.get(id = id)
    similar_product = get_similer_products(id ,20)
    return render(request, 'detail.html', {'product': _product, 'similar_products': similar_product})

