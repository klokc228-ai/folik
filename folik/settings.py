"""
Django settings for folik project (Ready for Render deployment, Cloudinary for media, multi-language support).
"""

from pathlib import Path
import os

# ── BASE DIR ──
BASE_DIR = Path(__file__).resolve().parent.parent

# ── SECURITY ──
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-replace-me')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'folik.onrender.com']

# ── APPLICATION DEFINITION ──
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Наше приложение
    'main',
    
    # Cloudinary
    'cloudinary',
    'cloudinary_storage',
]

# ── CLOUDINARY ──
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'RESOURCE_TYPE': 'image',
    'DEFAULT_TRANSFORMATION': [
        {'quality': 'auto'},
        {'fetch_format': 'auto'},
    ],
}

# ── MIDDLEWARE ──
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 🔥 для смены языка
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ── URLS ──
ROOT_URLCONF = 'folik.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # 🔥 нужен для смены языка
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'folik.wsgi.application'

# ── DATABASE (SQLite) ──
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── PASSWORD VALIDATION ──
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ── INTERNATIONALIZATION ──
LANGUAGE_CODE = 'uk'  # язык по умолчанию
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Поддерживаемые языки
LANGUAGES = [
    ('uk', 'Українська'),
    ('ru', 'Русский'),
]

LOCALE_PATHS = [
    BASE_DIR / 'main' / 'locale',
]

# ── STATIC FILES ──
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── MEDIA FILES ──
# media загружается на Cloudinary через DEFAULT_FILE_STORAGE

# ── DEFAULT AUTO FIELD ──
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── i18n REDIRECT AFTER LANGUAGE CHANGE ──
from django.utils.translation import gettext_lazy as _

# чтобы Django редиректил на предыдущую страницу после смены языка
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 1209600  # 2 недели
