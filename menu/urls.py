from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('produit/<int:product_id>/', views.product_detail, name='product_detail'),
]