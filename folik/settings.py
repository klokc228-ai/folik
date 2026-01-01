"""
Django settings for folik project.
Ready for Render + Cloudinary (updated 2026 compatible version)
"""

from pathlib import Path
import os

# ── BASE DIR ──
BASE_DIR = Path(__file__).resolve().parent.parent

# ── SECURITY ──
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set!")

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'folik.onrender.com']

# Добавляем render-овский домен динамически (на всякий случай)
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ── APPLICATION DEFINITION ──
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'main',                 # твое приложение
    
    'cloudinary',           # обязательно оставить
    'cloudinary_storage',   # пока оставляем, но ниже есть план Б
]

# ── CLOUDINARY CONFIG (самое важное) ──
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'SECURE': True,                    # https по умолчанию
    'STATIC_FILES': False,             # статику оставляем на whitenoise
}

# Современный способ для Django 4.2+ (очень рекомендуется!)
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Старый способ оставляем как fallback, но можно удалить позже
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ── MIDDLEWARE ──
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ── URLS & TEMPLATES ──
ROOT_URLCONF = 'folik.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'folik.wsgi.application'

# ── DATABASE (SQLite — нормально для небольшого проекта) ──
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── PASSWORD VALIDATION ──
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── INTERNATIONALIZATION ──
LANGUAGE_CODE = 'ru-ru'     # поменял на русский, если хочешь — верни 'en-us'
TIME_ZONE = 'Europe/Moscow' # или 'UTC'
USE_I18N = True
USE_TZ = True

# ── STATIC FILES ──
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── MEDIA (Cloudinary) ──
MEDIA_URL = '/media/'           # будет перенаправляться на cloudinary
# MEDIA_ROOT не нужен при использовании cloudinary

# ── DEFAULT AUTO FIELD ──
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Полезно для дебага (можно удалить потом) ──
if DEBUG:
    print("DEBUG mode ON")
    print(f"Cloudinary config: {CLOUDINARY_STORAGE}")