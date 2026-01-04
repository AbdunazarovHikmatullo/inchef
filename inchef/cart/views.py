from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Cart, CartItem
from product.models import Product


def get_or_create_cart(user):
    """Получить или создать корзину для пользователя"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_view(request):
    """Просмотр корзины"""
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('product', 'product__category').prefetch_related('product__images')
    
    context = {
        'cart': cart,
        'items': items,
        'total': cart.total_price(),
    }
    return render(request, 'cart/cart.html', context)


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_or_create_cart(request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1
    
    # Проверяем, есть ли уже этот товар в корзине
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Количество "{product.title}" увеличено в корзине.')
    else:
        messages.success(request, f'"{product.title}" добавлен в корзину!')
    
    # Если AJAX запрос - вернуть JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.title} добавлен в корзину',
            'cart_count': cart.items.count(),
            'cart_total': str(cart.total_price())
        })
    
    return redirect('product_detail', pk=product_id)


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Обновить количество товара в корзине"""
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Товар удалён из корзины.')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Количество обновлено.')
    
    return redirect('cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    
    product_title = cart_item.product.title
    cart_item.delete()
    
    messages.success(request, f'"{product_title}" удалён из корзины.')
    return redirect('cart')


@login_required
@require_POST
def clear_cart(request):
    """Очистить корзину"""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    
    messages.success(request, 'Корзина очищена.')
    return redirect('cart')
