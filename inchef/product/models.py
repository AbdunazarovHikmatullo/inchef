from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from account.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='products'
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    is_active = models.BooleanField(default=True)
    trashed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def move_to_trash(self):
        self.is_active = False
        self.trashed_at = timezone.now()
        self.save()
    
    def restore(self):
        self.is_active = True
        self.trashed_at = None
        self.save()
    
    def get_main_image(self):
        """Получить главное изображение или первое доступное"""
        main = self.images.filter(is_main=True).first()
        if main:
            return main
        return self.images.first()
    
    @property
    def average_rating(self):
        """Средний рейтинг продукта"""
        reviews = self.reviews.all()
        if not reviews:
            return None
        total = sum(review.grade for review in reviews)
        return round(total / len(reviews), 1)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продукта'

    def __str__(self):
        return f'Image for {self.product.title}'



class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    grade = models.PositiveSmallIntegerField(choices=[
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')
    ])
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'author')
