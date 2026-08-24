from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('menu/', include('menu.urls')),
    path('commandes/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# --- PERSONNALISATION DE L'ADMINISTRATION DJANGO ---
admin.site.site_header = "Chicken Tenders Dakar - Administration"  # En-tête principal en haut
admin.site.site_title = "Admin Chicken Tenders"                     # Titre de l'onglet du navigateur
admin.site.index_title = "Gestion du Restaurant & Commandes"       # Sous-titre de la page d'accueil admin

