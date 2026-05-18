import os
import datetime
from pathlib import Path
import socket 
from decouple import config
from django.core.exceptions import ImproperlyConfigured
from unipath import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def csv_config(name, default=""):
    return [item.strip() for item in config(name, default=default).split(",") if item.strip()]


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=config(
    'SECRET_KEY',
    default=os.environ.get("DJANGO_SECRET_KEY", "dev-insecure-secret-key-change-me" if DEBUG else None),
)

if not SECRET_KEY:
    raise ImproperlyConfigured("Set SECRET_KEY or DJANGO_SECRET_KEY when DEBUG is disabled.")

if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["10.0.2.2", "host.docker.internal", "47.128.216.140"]
    
# ALLOWED_HOSTS = [os.getenv("ALLOWED_PORTS")]
ALLOWED_HOSTS=csv_config('ALLOWED_HOSTS', default='localhost,127.0.0.1,[::1]')

# Cors Settings
BACKEND_DOMAIN=config('BACKEND_DOMAIN', default='http://localhost:8585/')
PAYMENT_SUCCESS_URL=config('PAYMENT_SUCCESS_URL', default=f'{BACKEND_DOMAIN.rstrip("/")}/api/v1/products/success/')
PAYMENT_CANCEL_URL=config('PAYMENT_CANCEL_URL', default=f'{BACKEND_DOMAIN.rstrip("/")}/api/v1/products/cancel/')
CORS_ORIGIN_ALLOW_ALL=config('CORS_ORIGIN_ALLOW_ALL', default=False, cast=bool)
STRIPE_PUBLISHABLE_KEY=config('STRIPE_PUBLISHABLE_KEY', default='')
STRIPE_SECRET_KEY=config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET=config('STRIPE_WEBHOOK_SECRET', default='')

CORS_ALLOWED_ORIGINS = csv_config('CORS_ALLOWED_ORIGINS') or [
    "http://127.0.0.1",
    "http://localhost",
]

CORS_ALLOW_CREDENTIALS=config('CORS_ALLOW_CREDENTIALS', default=False, cast=bool)

SECURE_SSL_REDIRECT=config('SECURE_SSL_REDIRECT', default=not DEBUG, cast=bool)
SESSION_COOKIE_SECURE=config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE=config('CSRF_COOKIE_SECURE', default=not DEBUG, cast=bool)
SECURE_HSTS_SECONDS=config('SECURE_HSTS_SECONDS', default=31536000 if not DEBUG else 0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS=config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=not DEBUG, cast=bool)
SECURE_HSTS_PRELOAD=config('SECURE_HSTS_PRELOAD', default=not DEBUG, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS='DENY'
DATA_UPLOAD_MAX_MEMORY_SIZE=config('DATA_UPLOAD_MAX_MEMORY_SIZE', default=2621440, cast=int)
FILE_UPLOAD_MAX_MEMORY_SIZE=config('FILE_UPLOAD_MAX_MEMORY_SIZE', default=2621440, cast=int)

# Django data browser
# References : https://pypi.org/project/django-data-browser/
DATA_BROWSER_FE_DSN=config('DATA_BROWSER_FE_DSN', default='')

# Application definition # # # # #
INSTALLED_APPS = [
    # 'django_tenants',
    # 'apps.app',  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "corsheaders",
    'graphene_django',
    'django_celery_results',
    'django_celery_beat',
    'django_filters',
    'drf_yasg',
    'widget_tweaks',
    'apps.home',
    'apps.snippets',
    'apps.users',
    'apps.finances',
    'apps.payments',
    'apps.products',
    'data_browser',
    'template_timings_panel'
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
        'django_extensions',
    ]


TENANT_APPS = ["client_app"]


# # Application definition # # # # #
# INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]

# TENANT_APPS = ["apps.home"]

# TENANT_MODEL = "app.Client"

# TENANT_DOMAIN_MODEL = "app.Domain"

# PUBLIC_SCHEMA_URLCONF = "app.urls"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "django_tenants.middleware.main.TenantMainMiddleware"
]

if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'debug_toolbar.panels.history.HistoryPanel',
        'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    ]

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
    "host.docker.internal",
    "172.104.60.217"
]

ROOT_URLCONF = 'multitenantsaas.urls'
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'multitenantsaas.wsgi.application'

#Connect to Neo4j Database
# config.DATABASE_URL = 'bolt://neo4j+s://f89c638e.databases.neo4j.io:7687'

# SQLite Database 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Database postgres Docker 
# Docker host : host.docker.internal  or database service name: prodxcloud-django-postgresdb
# docker inspect prodxcloud-django-postgresdb | grep "IPAddress"
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get("POSTGRES_NAME", "DB4"),
#         'USER': os.environ["POSTGRES_USER"],
#         'PASSWORD': os.environ["POSTGRES_PASSWORD"],
#         'HOST': os.environ.get("POSTGRES_HOST", "prodxcloud-django-postgresdb"),
#         'PORT': int(os.environ.get("POSTGRES_PORT", "5432")),
#     }
# }

# DATABASE_ROUTERS = (
#     'django_tenants.routers.TenantSyncRouter',
# )


# #Production / Development MYSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'DB2',
#         'USER': 'root',
#         'HOST': 'localhost',
#         'PASSWORD': '',
#         'PORT': '3306',
#     }
# }

# Password validation # #

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# JWT Authentification parameters
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
}
REST_FRAMEWORK = {

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')


# Internationalization #
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
IMAGES_DIR = os.path.join(MEDIA_ROOT, 'images')

if not os.path.exists(MEDIA_ROOT) or not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_PROFILE_MODULE = 'auth.User'
AUTH_USER_MODEL = 'auth.User'

# Extra places for collectstatic to find static files. #
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


# Caching parameters
# MEMUSAGE_ENABLED = True
# MEMUSAGE_LIMIT_MB = 2048
# C_FORCE_ROOT = 'true' 
# C_FORCE_ROOT = True

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': os.environ.get("BROKER_URL", "redis://redis:6379/1"),
#         "KEY_PREFIX": "DB2",
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }


#Celery parameters and Redis  Production parameters
CELERY_BROKER_URL=os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
CELERY_BROKER_TRANSPORT_URL=os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
# CELERY_RESULT_BACKEND= os.environ["CELERY_RESULT_BACKEND"]
BROKER_URL=os.environ.get("BROKER_URL", "redis://redis:6379/1")
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_TASK_SERIALIZER='json'
CELERY_RESULT_SERIALIZER='json'
CELERY_TIMEZONE="Asia/Singapore"
CELERY_TASK_TRACK_STARTED=True
CELERY_TASK_TIME_LIMIT=30 * 60
CELERY_TASK_ALWAYS_EAGER=True
CELERY_TASK_EAGER_PROPAGATES=True
CELERY_ALWAYS_EAGER=True
BROKER_HEARTBEAT= 10 
BROKER_HEARTBEAT_CHECKRATE =2.0
BROKER_POOL_LIMIT=None
BROKER_CONNECTION_RETRY=False
BROKER_CONNECTION_MAX_RETRIES=0
BROKER_CONNECTION_TIMEOUT=120
BROKER_CONNECTION_RETRY_ON_STARTUP=True
BROKER_CHANNEL_ERROR_RETRY=True
BROKER_TRANSPORT="kombu.transport.django"

#Parameters for SMTP EMAIL EmailBackend
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS=config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST=os.environ.get("EMAIL_HOST", "localhost")
EMAIL_HOST_USER=os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD=os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT=os.environ.get("EMAIL_PORT", 587)
