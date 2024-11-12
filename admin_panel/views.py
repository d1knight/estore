from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from category.models import Category, Attribute
from products.models import Product, ProductAttributeValue
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.core.paginator import Paginator


def admin_panel(request):
    return render(request,'admin_panel/admin_panel.html')



def category_list(request):
    category = Category.objects.all()
    paginator = Paginator(category, 3)  # Показать 5 авторов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'category/category_list.html',{'page_obj':page_obj})

def product_list(request):
    product = Product.objects.all()
    paginator = Paginator(product, 3)  # Показывать 4 продукта на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/product_list.html', {'page_obj': page_obj})



def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        slug = request.POST.get('slug')
        attributes = request.POST.getlist('attributes[]')  # Получаем список атрибутов из формы

        # Проверка на уникальность slug
        if Category.objects.filter(slug=slug).exists():
            error_message = "Категория с таким slug уже существует."
            return render(request, 'category/create_category.html', {'error_message': error_message})

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
            return render(request, 'category/create_category.html', {'error_message': error_message})

    return render(request, 'category/create_category.html')



def create_product(request):
    category_id = request.GET.get('category')  # Получаем выбранную категорию из GET-запроса
    categories = Category.objects.all()
    attributes = []

    # Если категория выбрана, загружаем атрибуты для этой категории
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        attributes = Attribute.objects.filter(category=category)

    if request.method == 'POST':
        # Получаем данные из формы
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')

        # Проверка на обязательные поля
        if not category_id or not name or not description or not price:
            messages.error(request, "Пожалуйста, заполните все обязательные поля.")
            return render(request, 'product/create_product.html', {
                'categories': categories,
                'attributes': attributes,
                'category_id': category_id,  # Передаем выбранную категорию
            })

        # Генерация slug
        slug = slugify(name)
        if Product.objects.filter(slug=slug).exists():
            slug = f"{slug}-{Product.objects.filter(slug__startswith=slug).count() + 1}"

        # Преобразование цены в число
        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Цена должна быть числовым значением.")
            return render(request, 'product/create_product.html', {
                'categories': categories,
                'attributes': attributes,
                'category_id': category_id,
            })

        # Создание продукта
        category = get_object_or_404(Category, id=category_id)
        product = Product.objects.create(
            category=category,
            name=name,
            description=description,
            price=price,
            image=image,
            image2=image2,
            image3=image3,
            image4=image4,
            slug=slug
        )

        # Добавление атрибутов
        for attribute in Attribute.objects.filter(category=category):
            value = request.POST.get(f'attribute_{attribute.id}')
            if value:
                ProductAttributeValue.objects.create(
                    product=product,
                    attribute=attribute,
                    value=value
                )

        messages.success(request, "Продукт успешно создан!")
        return redirect('admin_panel:product_list')  # Перенаправление на список продуктов

    return render(request, 'product/create_product.html', {
        'categories': categories,
        'attributes': attributes,
        'category_id': category_id,  # Передаем выбранную категорию обратно в форму
    })


def update_category(request,pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method=='POST':
        category.name = request.POST.get('name',category.name) # Сохранить текущее значение, если не указано
        category.description = request.POST.get('description', category.description)
        category.slug = request.POST.get('slug',category.slug)


        category.save()
        return redirect('admin_panel:category_list')
    return render(request,'category/update_category.html',{'category':category})



def delete_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_panel:category_list')
    return render(request,'category/delete_category.html',{'category':category})


