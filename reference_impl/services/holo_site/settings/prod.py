from .base import *

# Production: DEBUG désactivé
DEBUG = False

# Restreindre les hôtes (à adapter selon déploiement)
ALLOWED_HOSTS = ['dev.amg.km', 'localhost']

# Logging simplifié: niveau WARNING en root
LOGGING['root']['level'] = 'WARNING'

# Sécurité HTTPS pour déploiement derrière un proxy en prod
CSRF_TRUSTED_ORIGINS = ['https://dev.amg.km']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True