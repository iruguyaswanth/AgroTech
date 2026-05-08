"""
Buyers Forms
- Place Order
- Give Review
"""

from django import forms
from farmers.models import Order, Review


class PlaceOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity_kg', 'delivery_address', 'phone', 'note']
        widgets = {
            'quantity_kg': forms.NumberInput(attrs={'placeholder': 'How many kg?', 'step': '0.5', 'min': '0.5'}),
            'delivery_address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Full delivery address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Contact number'}),
            'note': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any special instructions? (optional)'}),
        }
        labels = {
            'quantity_kg': 'Quantity (kg)',
            'note': 'Note to Farmer',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your experience...'}),
        }
