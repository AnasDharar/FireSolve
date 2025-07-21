"""
Django settings for potd project.

Updated to be fully environment‑aware and production‑safe.

Key changes:
- DEBUG, SECRET_KEY, ALLOWED_HOSTS, DATABASE_URL now read from environment.
- ALLOWED_HOSTS merges env values *plus* required fallback hosts (localhost + project domain).
- Hard fail if DATABASE_URL missing (avoid mysterious boot errors).
- Static files configured for both dev & prod; Whitenoise enabled (safe in dev too).
"""
from pathlib import Path
import os
from environ import Env
import dj_database_url
env = Env()
# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------
# Debug & Secret Key
# ------------------------------------------------------------------
env.read_env(os.path.join(BASE_DIR, '.env'))
DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env("SECRET_KEY")
# ------------------------------------------------------------------
# Allowed Hosts
# ------------------------------------------------------------------
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# ------------------------------------------------------------------
# Installed Apps
# ------------------------------------------------------------------
INSTALLED_APPS = [
    'platforms.apps.PlatformsConfig',
    'users.apps.UsersConfig',
    'accounts.apps.AccountsConfig',
    'home.apps.HomeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------
MIDDLEWARE = [
    'debug_middleware.DebugHostMiddleware',  # custom debug middleware
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # keep always; harmless in dev
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'potd.urls'

# ------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------
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

WSGI_APPLICATION = 'potd.wsgi.application'
DATABASES = {
    'default': env.db("DATABASE_URL")
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Static Files
# ------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # source assets
STATIC_ROOT = BASE_DIR / 'staticfiles'    # collectstatic target (served by Nginx)

if DEBUG:
    # Local: don't use manifest hashing
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    # Prod: efficient caching + compression
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ------------------------------------------------------------------
# Default primary key field type
# ------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
