from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """Permet de voir la liste des articles à l'intérieur de la fiche de commande."""
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'unit_price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Configuration du suivi des commandes reçues."""
    list_display = ('id', 'customer_name', 'customer_phone', 'order_type', 'delivery_zone', 'total_amount', 'created_at')
    list_filter = ('order_type', 'created_at', 'delivery_zone')
    search_fields = ('customer_name', 'customer_phone', 'delivery_address')
    readonly_fields = ('total_amount', 'created_at')
    inlines = [OrderItemInline]  # Incorpore le détail du panier dans la commande