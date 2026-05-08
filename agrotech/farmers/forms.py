"""
Farmers Forms
- Add/Edit Crop
- Update Order Status
"""

from django import forms
from farmers.models import Crop, Order


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'category', 'description', 'price_per_kg', 'quantity_kg', 'location', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Fresh Tomatoes'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your crop — quality, harvest date, etc.'}),
            'price_per_kg': forms.NumberInput(attrs={'placeholder': 'Price in ₹ per kg', 'step': '0.01'}),
            'quantity_kg': forms.NumberInput(attrs={'placeholder': 'Available quantity in kg', 'step': '0.1'}),
            'location': forms.TextInput(attrs={'placeholder': 'Village / Taluk / District'}),
        }
        labels = {
            'price_per_kg': 'Price per kg (₹)',
            'quantity_kg': 'Available Quantity (kg)',
            'is_available': 'Mark as Available for Sale',
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'status-select'})
        }
