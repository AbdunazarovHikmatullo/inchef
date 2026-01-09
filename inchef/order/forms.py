from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'customer_phone', 'notes']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите адрес доставки'}),
            'customer_phone': forms.TextInput(attrs={'placeholder': '+992 ...'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Дополнительные пожелания к заказу'}),
        }
