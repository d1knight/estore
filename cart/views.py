from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from category.models import Category
from products.models import Product
from .models import Cart, CartItem

# Страница корзины
def view_cart(request):
    # Получаем одну корзину пользователя или создаем новую
    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(request, 'cart/view_cart.html', {'cart': cart})






def base_view(request):
    cart_item_count = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item_count = cart.items.count()  # Получаем количество товаров в корзине
        except Cart.DoesNotExist:
            cart = None

    return render(request, 'base.html', {'cart_item_count': cart_item_count, 'categories': Category.objects.all()})



@login_required
def add_to_cart(request, product_id):
    try:
        # Получаем продукт по ID
        product = Product.objects.get(id=product_id)

        # Получаем корзину пользователя или создаем новую, если ее нет
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Проверяем, есть ли уже этот продукт в корзине
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Если товар уже есть в корзине, увеличиваем его количество
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Перенаправляем пользователя в корзину
        return redirect('cart:view_cart')

    except Product.DoesNotExist:
        # Если продукт не найден, перенаправляем на страницу категории
        return redirect('products:category_list')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Обработка увеличения и уменьшения количества
    if request.method == "POST":
        action = request.POST.get("action")
        quantity = int(request.POST.get("quantity"))

        # Проверка на максимальное и минимальное количество
        if action == "increase" and quantity < 10:
            cart_item.quantity += 1
        elif action == "decrease" and quantity > 1:
            cart_item.quantity -= 1
        else:
            return HttpResponseBadRequest("Недопустимое количество.")

        cart_item.save()

        # Перенаправление обратно в корзину
        return redirect("cart:view_cart")

# Страница корзины с деталями
@login_required
def cart_detail(request):
    # Получаем корзину пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    return render(request, 'cart/cart_detail.html', {'cart': cart})




@login_required
def remove_cart_item(request, item_id):
    # Получаем объект CartItem
    item = get_object_or_404(CartItem, id=item_id)
    cart = item.cart

    # Удаляем товар из корзины
    item.delete()

    # Перенаправляем обратно в корзину
    return redirect('cart:view_cart')


def checkout(request):
    # Логика для оформления заказа
    return render(request, 'cart/checkout.html')  # Страница оформления заказа