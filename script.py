import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ProductRecommendation.settings'
django.setup()
import pandas as pd 
from product.models import product

import csv 
def fill_db_with_flipkart_com():
    csv_file_path = 'flipkart_com-ecommerce_sample.csv' 

    with open(csv_file_path, mode='r' , encoding='utf-8') as file:
        render = csv.DictReader(file)
        for row in render:
                try:
                    product_name = row['product_name']
                    product_image = eval(row['image'])[0]
                    description = row['description']
                    category = row['product_category_tree'].split('>>')[0].strip('[]"')
                    price = row['retail_price']
                    
                    print(product_image,product_image,description,category,price)
                    product.objects.update_or_create(
                    name = product_name,
                    defaults={
                    'product_image' : product_image,
                    'description' : description,
                    'category' : category,
                    'price' : price}
                    )
                    print('Data inserted successfully \n\n\n\n\n')
                except Exception as e:
                    print(e)
                    
                    
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from product.models import product

def get_similer_products(product_id, top_n=10):
    vectorizer = TfidfVectorizer(stop_words='english')
    product_description = product.objects.all().values_list('description', flat=True)
    tfid_matrix = vectorizer.fit_transform(product_description)
    target_product = product.objects.get(id=product_id)
    all_products = list(product.objects.all())
    target_index = all_products.index(target_product)
    cosine_simi = cosine_similarity(tfid_matrix[target_index], tfid_matrix).flatten()
    similer_indices = cosine_simi.argsort()[-top_n-1:-1][::-1]
    similer_indices = [i for i in similer_indices if i != target_index]
    similar_products = []
    for idx in similer_indices:
        similar_products.append(all_products[idx])
    return similar_products
    
    
print(get_similer_products(3092))