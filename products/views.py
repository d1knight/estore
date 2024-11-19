from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductAttributeValue
from category.models import Category, Attribute
from products.models import Product,ProductAttributeValue
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from category.models import Attribute

def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category).order_by('id')

    # Получаем параметры фильтрации
    search_query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Получаем выбранные атрибуты из запроса
    selected_attributes = request.GET.getlist('attributes')

    # Фильтрация по имени и описанию продукта
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Фильтрация по цене
    if min_price:
        try:
            min_price_value = Decimal(min_price.replace(' ', ''))
            products = products.filter(price__gte=min_price_value)
        except (ValueError, InvalidOperation):
            pass

    if max_price:
        try:
            max_price_value = Decimal(max_price.replace(' ', ''))
            products = products.filter(price__lte=max_price_value)
        except (ValueError, InvalidOperation):
            pass

    # Фильтрация по атрибутам


    if selected_attributes:
        selected_attributes = [str(attr) for attr in selected_attributes]  # Преобразуем в строку
        products = products.filter(
            Q(productattributevalue__value__in=selected_attributes)
    ).distinct()

    # Доступные атрибуты для категории
    category_attributes = Attribute.objects.filter(category=category)

    # Пагинация
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Форматируем цену
    for product in page_obj:
        product.price_display = f"{product.price:,.0f}".replace(',', ' ')

    return render(request, 'products/products_by_category.html', {
        'category': category,
        'page_obj': page_obj,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'category_attributes': category_attributes,
        'selected_attributes': selected_attributes,
    })

def product_detail(request, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=slug)
    
    # Получение значений атрибутов для продукта
    product_attributes = ProductAttributeValue.objects.filter(product=product)
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'category': category,
        'attributes': product_attributes,  # Передаем атрибуты в шаблон
    })



# products/views.py



def get_category_attributes(request):
    category_id = request.GET.get('category_id')
    if category_id:
        attributes = Attribute.objects.filter(category_id=category_id)
        attributes_list = [{'id': attr.id, 'name': attr.name} for attr in attributes]
        return JsonResponse(attributes_list, safe=False)
    return JsonResponse([], safe=False)


