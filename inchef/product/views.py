from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm, ProductImageFormSet


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



@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            formset.save_m2m()
            
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
        formset = ProductImageFormSet()

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Проверка прав доступа: только владелец может редактировать
    if request.user != product.owner:
        return redirect('product_detail', pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(request, 'product/edit_product.html', {
        'form': form,
        'formset': formset,
        'product': product
    })