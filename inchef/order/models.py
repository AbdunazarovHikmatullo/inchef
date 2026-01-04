from django.db import models
from django.conf import settings
from django.utils import timezone
from product.models import Product

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждён поваром'),
        ('picked_up', 'Забран курьером'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    )
    
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_orders',
        verbose_name='Клиент'
    )
    chef = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chef_orders',
        verbose_name='Повар'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Общая стоимость'
    )
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    customer_phone = models.CharField(max_length=20, verbose_name='Телефон клиента')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='Подтверждён')
    picked_up_at = models.DateTimeField(null=True, blank=True, verbose_name='Забран')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name='Доставлен')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Заказ #{self.id} от {self.customer.username}'
    
    def confirm(self):
        """Повар подтверждает заказ"""
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        self.save()
    
    def mark_picked_up(self):
        """Курьер забрал заказ"""
        self.status = 'picked_up'
        self.picked_up_at = timezone.now()
        self.save()
    
    def mark_delivered(self):
        """Заказ доставлен"""
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        self.save()
    
    def cancel(self):
        """Отменить заказ"""
        self.status = 'cancelled'
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Продукт'
    )
    product_title = models.CharField(max_length=255, verbose_name='Название блюда')
    product_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена за единицу')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f'{self.product_title} x{self.quantity}'
    
    def get_total_price(self):
        return self.product_price * self.quantity
    
    def save(self, *args, **kwargs):
        if not self.product_title:
            self.product_title = self.product.title
        if not self.product_price:
            self.product_price = self.product.price
        super().save(*args, **kwargs)
