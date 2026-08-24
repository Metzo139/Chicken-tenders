from pathlib import Path
from decouple import config, Csv
import os
from decouple import config
import dj_database_url
# 1. Emplacement racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Variables de sécurité (Lues depuis le fichier .env)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key')
DEBUG = True
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']

# 3. Applications activées dans le projet
INSTALLED_APPS = [
    'cloudinary_storage',
    'cloudinary',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Nos 4 applications modulaires
    'core',
    'menu',
    'orders',
    'pages',
]

# 4. Middlewares (Sécurité et gestion des fichiers statiques)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <--- Ajoute cette ligne ici
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurant_tenders.urls'

# 5. Configuration des dossiers de rendu HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Dossier HTML global du projet
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'restaurant_tenders.wsgi.application'

# 6. Base de données par défaut (SQLite pour le développement local)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_xh8I0YpqynOi@ep-little-sunset-aygfv2zh-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'),
        conn_max_age=600,
        ssl_require=True
    )
}
# 7. Regles de sécurité des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 8. Internationalisation (Langue française et heure de Dakar)
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Dakar'
USE_I18N = True
USE_TZ = True

# 9. Fichiers Statiques (CSS, JavaScript, Logos)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Fichiers statiques (CSS, JS)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Fichiers médias (Images uploadées par les utilisateurs)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Type d'identifiant par défaut des modèles
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dnu2uzbsw',
    'API_KEY': '972289414882153',
    'API_SECRET': 'o6cMpIkfs7AbDogP1fWQL_u3bt4',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

