from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, product_id):
    """Affiche la fiche d'un plat avec le choix des sauces et extras."""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    sauces = product.sauces.all()
    extras = product.extras.all()

    context = {
        'product': product,
        'sauces': sauces,
        'extras': extras,
    }
    return render(request, 'menu/product_detail.html', context)