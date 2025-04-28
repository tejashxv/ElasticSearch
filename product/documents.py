from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import product

@registry.register_document
class Product_document(Document):
    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    class Django:
        model = product
        fields = [
            'name',
            "product_image",
            'description',
            'category',
            'price',
            'created_at',
            
        ]