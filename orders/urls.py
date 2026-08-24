from django.urls import path
from . import views

app_name = 'orders'  # <--- Définit l'espace de noms utilisé par {% url 'orders:...' %}

urlpatterns = [
    path('panier/', views.cart_detail, name='cart_detail'),
    path('panier/ajouter/<int:product_id>/', views.cart_add, name='cart_add'),
    path('panier/supprimer/<str:item_key>/', views.cart_remove, name='cart_remove'),
    path('valider/', views.checkout, name='checkout'),
]