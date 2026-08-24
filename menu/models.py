from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    slug = models.SlugField(unique=True, help_text="Identifiant unique pour l'URL (ex: chicken-tenders)")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.name


class Sauce(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la sauce")
    additional_price = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, verbose_name="Prix supplémentaire (FCFA)"
    )

    class Meta:
        verbose_name = "Sauce"
        verbose_name_plural = "Sauces"

    def __str__(self):
        return f"{self.name} (+{self.additional_price} FCFA)" if self.additional_price > 0 else self.name


class Extra(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de l'extra")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Prix (FCFA)")

    class Meta:
        verbose_name = "Extra"
        verbose_name_plural = "Extras"

    def __str__(self):
        return f"{self.name} (+{self.price} FCFA)"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Catégorie")
    name = models.CharField(max_length=150, verbose_name="Nom du produit")
    description = models.TextField(blank=True, verbose_name="Description du plat")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Prix de base (FCFA)")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Photo du plat")
    is_available = models.BooleanField(default=True, verbose_name="Disponible à la vente")

    sauces = models.ManyToManyField(Sauce, blank=True, verbose_name="Sauces associables")
    extras = models.ManyToManyField(Extra, blank=True, verbose_name="Extras associables")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.name