from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from .models import Product, Category


def products(request):
    """Каталог продуктов с фильтрацией и поиском"""
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '-created_at')

    products_qs = (
        Product.objects
        .filter(is_active=True)
        .select_related('category', 'owner')
        .prefetch_related('images', 'reviews')
    )

    if category_slug:
        products_qs = products_qs.filter(category__slug=category_slug)
    
    if search_query:
        products_qs = products_qs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    valid_sorts = ['price', '-price', 'created_at', '-created_at', 'title']
    if sort_by in valid_sorts:
        products_qs = products_qs.order_by(sort_by)

    categories = Category.objects.all()

    context = {
        'products': products_qs,
        'categories': categories,
        'active_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }

    return render(request, 'product/products.html', context)


def product_detail(request, pk):
    """Детальная страница продукта"""
    product = get_object_or_404(
        Product.objects
        .select_related('category', 'owner', 'owner__profile')
        .prefetch_related('images', 'reviews__author'),
        pk=pk,
        is_active=True
    )
    
    avg_rating = product.reviews.aggregate(avg=Avg('grade'))['avg']
    
    related_products = (
        Product.objects
        .filter(category=product.category, is_active=True)
        .exclude(pk=product.pk)
        .prefetch_related('images')[:4]
    )

    context = {
        'product': product,
        'images': product.images.all(),
        'reviews': product.reviews.all().order_by('-created_at')[:10],
        'average_rating': round(avg_rating, 1) if avg_rating else None,
        'reviews_count': product.reviews.count(),
        'related_products': related_products,
    }

    return render(request, 'product/product_detail.html', context)



def create_product(request):
    
    return render(request, 'product/create_product.html')