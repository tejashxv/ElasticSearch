import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ProductRecommendation.settings'
django.setup()
import pandas as pd 
from product.models import product

import csv 
csv_file_path = 'flipkart_com-ecommerce_sample.csv' 

with open(csv_file_path, mode='r' , encoding='utf-8') as file:
    render = csv.DictReader(file)
    
    for row in render:
        # try:
        product_name = row['product_name']
        product_image = eval(row['image'])[0]
        description = row['description']
        category = row['product_category_tree'].split('>>')[0].strip('[]"')
        price = row['retail_price']
        
        print(product_image,product_image,description,category,price)
        product.objects.create(product_image = product_image,
        name = product_name,
        description = description,
        category = category,
        price = price
        )