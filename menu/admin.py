from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Sauce, Extra

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configuration de l'administration des catégories."""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Génère automatiquement le slug à partir du nom
    search_fields = ('name',)

@admin.register(Sauce)
class SauceAdmin(admin.ModelAdmin):
    """Configuration des sauces."""
    list_display = ('name', 'additional_price')
    search_fields = ('name',)

@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    """Configuration des extras."""
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Configuration avancée des produits (Tenders, Burgers, etc.)."""
    list_display = ('display_image', 'name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    list_editable = ('price', 'is_available')  # Permet d'éditer le prix et la disponibilité directement depuis la liste
    search_fields = ('name', 'description')
    filter_horizontal = ('sauces', 'extras')  # Interface fluide pour associer sauces et extras

    def display_image(self, obj):
        """Affiche une miniature de l'image du produit dans le tableau."""
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px; border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    display_image.short_description = 'Visuel'