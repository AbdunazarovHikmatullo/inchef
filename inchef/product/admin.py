from django.contrib import admin
from .models import Category, Product, ProductImage, Review


# ---------- Inline ----------

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('author', 'grade', 'created_at')


# ---------- Category ----------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


# ---------- Product ----------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'category',
        'price',
        'is_active',
        'created_at',
        'trashed_at',
    )

    list_filter = (
        'is_active',
        'category',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'owner__username',
    )

    readonly_fields = (
        'created_at',
        'trashed_at',
    )

    inlines = (
        ProductImageInline,
        ReviewInline,
    )

    actions = ('move_to_trash', 'restore_from_trash')

    def move_to_trash(self, request, queryset):
        for product in queryset:
            product.move_to_trash()
        self.message_user(request, 'Выбранные продукты перемещены в trash')

    move_to_trash.short_description = 'Переместить в trash'

    def restore_from_trash(self, request, queryset):
        updated = queryset.update(is_active=True, trashed_at=None)
        self.message_user(request, f'Восстановлено: {updated} продуктов')

    restore_from_trash.short_description = 'Восстановить из trash'


# ---------- Review ----------

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'grade', 'created_at')
    list_filter = ('grade', 'created_at')
    search_fields = ('product__title', 'author__username')
    readonly_fields = ('created_at',)
