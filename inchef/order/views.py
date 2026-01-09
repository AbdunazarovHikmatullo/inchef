from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cart.views import get_or_create_cart
from .models import Order, OrderItem
from .forms import OrderCreateForm

@login_required
def create_order(request):
    cart = get_or_create_cart(request.user)
    if not cart.items.exists():
        return redirect('products')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Группируем товары по поварам
            cart_items = cart.items.select_related('product', 'product__owner').all()
            
            # Словарь: {chef_user: [list_of_cart_items]}
            items_by_chef = {}
            for item in cart_items:
                chef = item.product.owner
                if chef not in items_by_chef:
                    items_by_chef[chef] = []
                items_by_chef[chef].append(item)
            
            # Создаем заказы в транзакции
            with transaction.atomic():
                for chef, items in items_by_chef.items():
                    # Считаем общую сумму для этого повара
                    total_price = sum(item.total_price() for item in items)
                    
                    order = Order.objects.create(
                        customer=request.user,
                        chef=chef,
                        total_price=total_price,
                        delivery_address=form.cleaned_data['delivery_address'],
                        customer_phone=form.cleaned_data['customer_phone'],
                        notes=form.cleaned_data['notes']
                    )
                    
                    for item in items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            product_title=item.product.title,
                            product_price=item.product.price,
                            quantity=item.quantity
                        )
                
                # Очищаем корзину после успешного создания заказов
                cart.items.all().delete()
                
            return render(request, 'order/created.html')
    else:
        form = OrderCreateForm()

    return render(request, 'order/create.html', {
        'cart': cart,
        'form': form,
        'username': request.user.username # Just explicit pass if needed
    })
