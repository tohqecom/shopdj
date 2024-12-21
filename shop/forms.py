﻿from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'city', 'postal_code', 'country', 'payment_method']
        widgets = {
            'payment_method': forms.RadioSelect,  # Sử dụng nút radio cho phương thức thanh toán
        }
