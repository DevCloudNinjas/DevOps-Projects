import os
import datetime
from pathlib import Path
import socket 
from decouple import config
from unipath import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY', default='54g6s%qjfnhbpw0zeoei=$!her*y(p%!&84rs$4l85io')
SECRET_KEY=config('SECRET_KEY', default = os.environ.get("DJANGO_SECRET_KEY", "54g6s%qjfnhbpw0zeoei=$!her*y(p%!&84rs$4l85io"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=config('DEBUG', default=True, cast=bool)

if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["10.0.2.2", "host.docker.internal", "47.128.216.140"]
    
# ALLOWED_HOSTS = [os.getenv("ALLOWED_PORTS")]
ALLOWED_HOSTS=['*']

# Cors Settings
BACKEND_DOMAIN='http://172.104.60.217:8585/'
PAYMENT_SUCCESS_URL='http://172.104.60.217:8585/api/v1/products/success/'
PAYMENT_CANCEL_URL='http://172.104.60.217:8585/api/v1/products/cancel/'
CORS_ORIGIN_ALLOW_ALL=True

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
    "https://792jz173sj.execute-api.us-east-1.amazonaws.com",
    "https://socialcloudsync.com",
    "http://52.90.4.135",
    "http://52.90.4.135:8585"
]

CORS_ALLOW_CREDENTIALS=True

# Django data browser
# References : https://pypi.org/project/django-data-browser/
DATA_BROWSER_FE_DSN="https://af64f22b81994a0e93b82a32add8cb2b@o390136.ingest.sentry.io/5231151"

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
    'debug_toolbar',
    'django_extensions',
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


TENANT_APPS = ["client_app"]


# # Application definition # # # # #
# INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]

# TENANT_APPS = ["apps.home"]

# TENANT_MODEL = "app.Client"

# TENANT_DOMAIN_MODEL = "app.Domain"

# PUBLIC_SCHEMA_URLCONF = "app.urls"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "django_tenants.middleware.main.TenantMainMiddleware"
]

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
#         'USER': os.environ.get("POSTGRES_USER", "postgres"),
#         'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "postgres"),
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
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    # ), 
}


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
# CELERY_RESULT_BACKEND= os.environ.get("CELERY_RESULT_BACKEND", "db+postgresql://postgres:postgres@172.104.60.217/DB2") 
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
EMAIL_USE_TLS=os.environ.get("EMAIL_USE_TLS", True)
EMAIL_HOST=os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_HOST_USER=os.environ.get("EMAIL_HOST_USER", "notifyprodtestemail1@gmail.com")
EMAIL_HOST_PASSWORD=os.environ.get("EMAIL_HOST_PASSWORD", "Michael@5151")
EMAIL_PORT=os.environ.get("EMAIL_PORT", 587)
