# cart/context_processors.py
from .models import Cart

def cart_item_count(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item_count = cart.items.count()  # Количество товаров в корзине
        except Cart.DoesNotExist:
            cart_item_count = 0
    return {'cart_item_count': cart_item_count}
