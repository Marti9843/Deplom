import os
from pathlib import Path
from django.urls import reverse_lazy

# Основні налаштування
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-l6_3#c(!#2_520w#abnl41c-23=)uvu0w80m^7qxxz3&1!c_=i'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Час життя токена підтвердження у годинах
EMAIL_VERIFICATION_EXPIRE_HOURS = 24

# Налаштування кешу
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Налаштування сайту
SITE_ID = 1
SITE_NAME = "Sport Center"
SITE_DOMAIN = "localhost:8000"  # Змініть на ваш домен у продакшені

# Додатки
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Локальні додатки
    'accounts.apps.AccountsConfig',
    'navigation.apps.NavigationConfig',
    'pages.apps.PagesConfig',
    'services.apps.ServicesConfig',
    'news.apps.NewsConfig',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL конфігурація
ROOT_URLCONF = 'sport_center.urls'

# Шаблони
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'accounts/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'navigation.context_processors.navigation_items',
                'accounts.context_processors.email_verification',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'sport_center.wsgi.application'

# База даних
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_booking',
        'USER': 'postgres',
        'PASSWORD': '1337',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Валідатори паролів
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Міжнароднізація
LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статика та медіа
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Аутентифікація
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = reverse_lazy('accounts:login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('home')

# Налаштування email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mistervadic@gmail.com'
EMAIL_HOST_PASSWORD = 'smys ixfo cbrp jpaa'  # Пароль додатка
DEFAULT_FROM_EMAIL = 'Sport Center <mistervadic@gmail.com>'
SERVER_EMAIL = 'mistervadic@gmail.com'

# Конфігурація підтвердження email
EMAIL_VERIFICATION_EXPIRE_DAYS = 3  # Термін дії посилання для підтвердження
EMAIL_VERIFICATION_SUBJECT = "Підтвердження email для Sport Center"
EMAIL_VERIFICATION_HTML_TEMPLATE = 'accounts/email_verification_email.html'
EMAIL_VERIFICATION_TEXT_TEMPLATE = 'accounts/email_verification_email.txt'

# Інші налаштування
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Налаштування безпеки для продакшену
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'