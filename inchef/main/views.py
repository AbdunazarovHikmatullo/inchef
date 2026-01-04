from django.shortcuts import render
from product.models import Product

def index(request):
    """Главная страница с последними товарами"""
    latest_products = (
        Product.objects
        .filter(is_active=True)
        .select_related('owner', 'category')
        .prefetch_related('images', 'reviews')
        .order_by('-created_at')[:8]  # Показываем 8 для ровной сетки
    )
    
    context = {
        'latest_products': latest_products,
    }
    return render(request, 'main/index.html', context)