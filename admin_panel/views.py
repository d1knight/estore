import re
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from category.models import Category, Attribute
from products.models import Product, ProductAttributeValue
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout,login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from unidecode import unidecode


def admin_panel(request):
    return render(request,'admin_panel/admin_panel.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Вы можете войти в систему.')
            return redirect('admin_panel:login') 
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'admin_panel/register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)


        if user is not None:
            auth_login(request, user)  # Используем alias auth_login
            return redirect('admin_panel:admin_panel')
        else:
            messages.error(request, "Неправильное имя пользователя или пароль.")

    return render(request, 'admin_panel/login.html')


def logout_view(request):
    logout(request)
    return redirect('main')

@login_required
def category_list(request):
    category = Category.objects.all()
    paginator = Paginator(category, 3)  # Показать 5 авторов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'category/category_list.html',{'page_obj':page_obj})


@login_required
def product_list(request):
    search_query = request.GET.get('search', '')  # Получение строки поиска из GET-параметров
    products = Product.objects.all()
    
    # Фильтрация по названию, если указан поисковый запрос
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Пагинация
    paginator = Paginator(products, 3)  # Показывать 3 продукта на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product/product_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,  # Передаем строку поиска в шаблон
    })


@login_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        slug = request.POST.get('slug')  # Получаем слаг из формы
        attributes = request.POST.getlist('attributes[]')  # Получаем список атрибутов из формы

        # Если слаг не был введён, автоматически создаём его на основе имени категории
        if not slug:
            slug = generate_slug(name)

        # Проверка на уникальность slug
        if Category.objects.filter(slug=slug).exists():
            error_message = "Категория с таким slug уже существует."
            return render(request, 'category/create_category.html', {'error_message': error_message, 'name': name, 'description': description, 'slug': slug})

        try:
            # Создаем категорию
            category = Category.objects.create(
                name=name,
                description=description,
                slug=slug,
            )

            # Создаем атрибуты для категории, если они указаны
            for attribute_name in attributes:
                if attribute_name.strip():  # Проверяем, что атрибут не пустой
                    Attribute.objects.create(
                        name=attribute_name.strip(),
                        category=category
                    )

            return redirect('admin_panel:category_list')
        except IntegrityError:
            error_message = "Ошибка при сохранении категории."
            return render(request, 'category/create_category.html', {'error_message': error_message, 'name': name, 'description': description, 'slug': slug})

    return render(request, 'category/create_category.html')


# Функция для генерации слага на основе имени
def generate_slug(name):
    slug = name.lower()
    slug = slug.strip()
    slug = re.sub(r'\s+', '-', slug)  # Заменить пробелы на дефисы
    slug = re.sub(r'[^\w\-]+', '', slug)  # Удалить все неалфавитные символы
    return slug


@login_required
def create_product(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category') or request.POST.get('category')
    attributes = Attribute.objects.filter(category_id=category_id) if category_id else []

    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')

        # Валидация данных
        if not category_id or not name or not description or not price:
            messages.error(request, "Заполните все обязательные поля.")
            return render(request, 'product/create_product.html', {
                'categories': categories,
                'attributes': attributes,
                'category_id': category_id,
            })

        # Создание продукта
        slug = slugify(unidecode(name))
        if Product.objects.filter(slug=slug).exists():
            slug = f"{slug}-{Product.objects.filter(slug__startswith=slug).count() + 1}"

        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Цена должна быть числом.")
            return render(request, 'product/create_product.html', {
                'categories': categories,
                'attributes': attributes,
                'category_id': category_id,
            })

        product = Product.objects.create(
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            slug=slug,
            image=image,
            image2=image2,
            image3=image3,
            image4=image4
        )

        # Сохранение атрибутов
        for attribute in attributes:
            value = request.POST.get(f'attribute_values-{attribute.id}-value')
            if value:
                ProductAttributeValue.objects.create(
                    product=product,
                    attribute=attribute,
                    value=value
                )

        messages.success(request, "Продукт успешно создан.")
        return redirect('admin_panel:product_list')

    return render(request, 'product/create_product.html', {
        'categories': categories,
        'attributes': attributes,
        'category_id': category_id,
    })

@login_required
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    attributes = category.attributes.all()  # Получаем атрибуты категории

    if request.method == 'POST':
        # Обновление полей категории
        category.name = request.POST.get('name', category.name)
        category.description = request.POST.get('description', category.description)
        category.slug = request.POST.get('slug', category.slug)
        category.save()

        # Обновление значений атрибутов
        for attribute in attributes:
            new_value = request.POST.get(f'attribute_{attribute.id}')
            if new_value:
                attribute.name = new_value
                attribute.save()

        return redirect('admin_panel:category_list')

    return render(request, 'category/update_category.html', {'category': category, 'attributes': attributes})


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    category_attributes = product.category.attributes.all()  # Получаем атрибуты категории

    if request.method == 'POST':
        # Обновляем основные поля продукта
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.slug = request.POST.get('slug', product.slug)
        product.price = request.POST.get('price', product.price)

        # Обновляем изображения, если они переданы
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        if 'image2' in request.FILES:
            product.image2 = request.FILES['image2']
        if 'image3' in request.FILES:
            product.image3 = request.FILES['image3']
        if 'image4' in request.FILES:
            product.image4 = request.FILES['image4']

        product.save()  # Сохраняем изменения продукта

        # Сохранение значений атрибутов
        for attribute in category_attributes:
            value = request.POST.get(f'attribute_{attribute.id}')
            if value:
                ProductAttributeValue.objects.update_or_create(
                    product=product,
                    attribute=attribute,
                    defaults={'value': value}
                )

        return redirect('admin_panel:product_list')  # Перенаправление после обновления

    # Получаем текущие значения атрибутов для отображения в форме

    attribute_values = {
    attr.attribute_id: attr.value
    for attr in product.attribute_values.all()
}

    return render(request, 'product/update_product.html', {
        'product': product,
        'category_attributes': category_attributes,
        'attribute_values': attribute_values,
    })


@login_required
def delete_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_panel:category_list')
    return render(request,'category/delete_category.html',{'category':category})


@login_required
def delete_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_panel:product_list')
    return render(request,'product/delete_product.html',{'product':product})

