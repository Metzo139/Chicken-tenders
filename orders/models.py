from django.db import models
from menu.models import Product, Sauce, Extra

class Order(models.Model):
    ORDER_TYPES = (
        ('delivery', 'Livraison à domicile'),
        ('takeaway', 'À emporter'),
    )

    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    )

    customer_name = models.CharField(max_length=100, verbose_name="Nom du client")
    customer_phone = models.CharField(max_length=20, verbose_name="Téléphone WhatsApp")
    customer_email = models.EmailField(blank=True, null=True, verbose_name="Email (Optionnel)")
    
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, default='delivery', verbose_name="Type de commande")
    delivery_zone = models.CharField(max_length=100, blank=True, verbose_name="Zone de livraison (ex: Mermoz, Plateau)")
    delivery_address = models.TextField(blank=True, verbose_name="Adresse / Repère de livraison")
    notes = models.TextField(blank=True, verbose_name="Instructions particulières")

    total_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Montant total (FCFA)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return f"Commande #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Commande")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produit")
    sauce = models.ForeignKey(Sauce, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sauce choisie")
    extras = models.ManyToManyField(Extra, blank=True, verbose_name="Extras choisis")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    unit_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Prix unitaire appliqué (FCFA)")

    class Meta:
        verbose_name = "Article commandé"
        verbose_name_plural = "Articles commandés"

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"