from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'order_type', 'delivery_zone', 'delivery_address', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ex: Ablaye Diallo'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ex: 77 123 45 67'}),
            'order_type': forms.Select(attrs={'class': 'form-select rounded-pill'}),
            'delivery_zone': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ex: Mermoz, Almadies, Plateau'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 2, 'placeholder': 'Indiquez un point de repère précis'}),
            'notes': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 2, 'placeholder': 'Ex: Pas de sauce piquante'}),
        }