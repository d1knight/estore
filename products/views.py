from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category).order_by('id')

    # Получаем параметры фильтрации из запроса
    search_query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Фильтрация по названию, игнорируя регистр
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Фильтрация по минимальной и максимальной цене
    if min_price:
        try:
            min_price_value = Decimal(min_price.replace(' ', ''))  # Удаление пробелов и преобразование
            products = products.filter(price__gte=min_price_value)  # Включаем минимальную цену
        except (ValueError, InvalidOperation):
            pass  # Игнорируем некорректные значения

    if max_price:
        try:
            max_price_value = Decimal(max_price.replace(' ', ''))  # Удаление пробелов и преобразование
            products = products.filter(price__lte=max_price_value)  # Исключаем максимальную цену
        except (ValueError, InvalidOperation):
            pass  # Игнорируем некорректные значения

    # Пагинация
    paginator = Paginator(products, 8)  # Показывать 8 продуктов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Преобразуем цены в строки и заменяем запятые на пробелы
    for product in page_obj:
        product.price_display = f"{product.price:,.0f}".replace(',', ' ')

    return render(request, 'products/products_by_category.html', {
        'category': category, 
        'page_obj': page_obj,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
    })


def product_detail(request, category_slug, slug):
    # Получаем категорию по slug
    category = get_object_or_404(Category, slug=category_slug)
    # Получаем продукт по slug
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'category': category,
    })
