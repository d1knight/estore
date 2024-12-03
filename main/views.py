from django.shortcuts import render, get_object_or_404
from products.models import Product  # или другой путь к модели, если она находится в другом приложении
from django.core.paginator import Paginator
from category.models import Category
from products.models import Product
from cart.models import Cart
from django.core.paginator import Paginator
from django.shortcuts import render


from django.core.paginator import Paginator
from django.shortcuts import render

def main(request):
    # Логика для корзины
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item_count = cart.items.count()  # Количество товаров в корзине
        except Cart.DoesNotExist:
            cart_item_count = 0

    # Логика для поиска продуктов
    query = request.GET.get('q', '')

    # Получаем все категории
    categories = Category.objects.all()
    categories_with_products = {}

    for category in categories:
        products = Product.objects.filter(category=category)

        # Применяем поиск, если запрос указан
        if query:
            products = products.filter(name__icontains=query)

        # Добавляем категорию в результат только если есть продукты
        if products.exists():
            paginator = Paginator(products, 4)  # Показываем 4 продукта на страницу
            page_number = request.GET.get(f'page_{category.id}', 1)
            page_obj = paginator.get_page(page_number)
            categories_with_products[category] = page_obj

    return render(request, 'main/index.html', {
        'categories_with_products': categories_with_products,
        'query': query,
        'cart_item_count': cart_item_count,  # Передаем количество товаров в корзине
    })



def search_results(request):
    query = request.GET.get('q', '').strip()  # Получаем строку поиска
    categories_with_products = {}

    if query:  # Если есть запрос
        categories = Category.objects.all()
        for category in categories:
            products = Product.objects.filter(
                category=category,
                name__icontains=query
            )  # Фильтруем продукты по категории и запросу
            if products.exists():
                categories_with_products[category] = products

    return render(request, 'main/search_results.html', {
        'categories_with_products': categories_with_products,
        'query': query,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Получаем продукт по pk
    return render(request, 'products/product_detail.html', {'product': product})