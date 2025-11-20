import os
from pathlib import Path

# Répertoire racine du projet (services/) -> 3 niveaux au-dessus de ce fichier
BASE_DIR = Path(__file__).resolve().parents[2]

SECRET_KEY = 'dev-secret-key-change-me'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'holo_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'payments' / 'templates'],
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

WSGI_APPLICATION = 'holo_site.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'payments' / 'static'
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- HOLO / AMG settings ---
HOLO_BASE_URL = os.environ.get('HOLO_BASE_URL', 'https://26900.tagpay.fr')
HOLO_ONLINE_ENDPOINT = os.environ.get('HOLO_ONLINE_ENDPOINT', '/online/online.php')
HOLO_MERCHANT_ID = os.environ.get('HOLO_MERCHANT_ID', '2449462108576891')
HOLO_CURRENCY = 174

# Permettre d'imposer un mode manuel (pas d'auto-submit) pour les tests/recette
HOLO_FORCE_MANUAL = os.environ.get('HOLO_FORCE_MANUAL', 'false').lower() in ('1', 'true', 'yes', 'on')

CALLBACK_DOMAIN = os.environ.get('CALLBACK_DOMAIN', 'https://dev.amg.km')

NOTIFY_URL = f"{CALLBACK_DOMAIN}/holo/notificationpaiement"
ACCEPT_URL = f"{CALLBACK_DOMAIN}/holo/acceptpaiement"
DECLINE_URL = f"{CALLBACK_DOMAIN}/holo/declinepaiement"
CANCEL_URL = f"{CALLBACK_DOMAIN}/holo/cancelpaiement"

IP_WHITELIST = os.environ.get('IP_WHITELIST', '3.6.76.175').split(',')
SIGNING_SECRET = os.environ.get('SIGNING_SECRET', 'change-me')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'journal.log',
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}