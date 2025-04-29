from django.shortcuts import render, redirect
from .models import product
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from .productRecommender import get_similer_products
from django_elasticsearch_dsl.search import Search
from .documents import Product_document
from django.http import JsonResponse
# Create your views here.
class ProductsAPI(APIView):
    def get(self, request):
        q = request.GET.get('q', '')
        if q:
            _product = product.objects.filter(name__icontains=q).values_list('name', flat=True).distinct()[:10]
            return Response({'suggestions': list(_product)})
        else:
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
    products = product.objects.all().order_by('?')[:40]
    if request.method == 'GET':
        if request.GET.get('q'):
            return redirect(f"{reverse('search_product')}?{urlencode({'q': request.GET.get('q')})}")
    return render(request, 'home.html', {'product': products})

def product_detail(request, id):
    _product = product.objects.get(id = id)
    similar_product = get_similer_products(id ,20)
    if request.method == 'GET':
        if request.GET.get('q'):
            return redirect(f"{reverse('search_product')}?{urlencode({'q': request.GET.get('q')})}")
    return render(request, 'detail.html', {'product': _product, 'similar_products': similar_product})

def search_product(request):
    data = {
        "status": 200,
        "message": "success",
        "products": [],
    }
    if request.method == 'GET':
        if request.GET.get('q'):
            search = request.GET.get('q')
            result = Product_document.search().query(
            'multi_match',
            query=search,
            fields=['name', 'description', 'category'],
            fuzziness='AUTO'
            ).extra(size=200)
            products = []
            result = result.execute()
            data['results'] = [hit.to_dict() for hit in result]
            for hit in result:
                products.append({ 
                        'id': hit.meta.id,
                        'name' : hit.name ,
                        'product_image' : hit.product_image ,
                        'description' : hit.description ,
                        'category' : hit.category ,
                        'price' : hit.price ,
                        'created_at' : hit.created_at,
                })
            data['products'] = products
            
            # return JsonResponse(data, safe=False)
        return render(request, 'search.html', {'product': data['products'], 'search': request.GET.get('q')})

        
            
    