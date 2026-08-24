from django.shortcuts import render
from menu.models import Product, Category

def home(request):
    """Affiche la page d'accueil avec les catégories et les produits phares."""
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_available=True)
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'pages/home.html', context)

def about(request):
    """Affiche la page À propos du restaurant."""
    return render(request, 'pages/about.html')