from django.shortcuts import render, get_object_or_404
from .models import Category
from products.models import Product  # Замените your_app на название приложения, где находится модель Product

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category/category_products.html', {'category': category, 'products': products})
