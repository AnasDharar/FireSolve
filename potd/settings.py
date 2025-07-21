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
import dj_database_url

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Debug & Secret Key
# ------------------------------------------------------------------
DEBUG = os.getenv("DEBUG", "False").lower() in {"true", "1", "yes", "on"}

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-default-key-change-this"  # fallback only; override via env in prod
)

# ------------------------------------------------------------------
# Allowed Hosts
# ------------------------------------------------------------------
# Preferred env var name: ALLOWED_HOSTS (comma-separated).
# Backward compat: DJANGO_ALLOWED_HOSTS.
_env_hosts_raw = os.getenv("ALLOWED_HOSTS") or os.getenv("DJANGO_ALLOWED_HOSTS")

# Hosts we ALWAYS allow for safety (local + your domain)
_required_hosts = [
    "127.0.0.1",
    "localhost",
    "firesolve.salaar.tech",
    "www.firesolve.salaar.tech",
]

if _env_hosts_raw:
    _env_hosts = [h.strip() for h in _env_hosts_raw.split(",") if h.strip()]
    # Preserve order, dedupe
    _seen = set()
    ALLOWED_HOSTS = []
    for h in _env_hosts + _required_hosts:
        if h not in _seen:
            _seen.add(h)
            ALLOWED_HOSTS.append(h)
else:
    ALLOWED_HOSTS = _required_hosts.copy()

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

# ------------------------------------------------------------------
# Database (Neon / Postgres via DATABASE_URL)
# ------------------------------------------------------------------
_db_url = os.getenv("DATABASE_URL")
if not _db_url:
    raise RuntimeError("DATABASE_URL environment variable is required but not set.")

DATABASES = {
    'default': dj_database_url.parse(_db_url, ssl_require=True, conn_max_age=600),
}

# ------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------
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
