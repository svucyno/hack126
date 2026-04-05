"""
Django settings for DripFit backend.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Paths & env
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-changeme")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") + ["testserver"]

# -------------------------------------------------------------------
# Installed apps
# -------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",           # required by allauth
    # Third-party
    "rest_framework",
    "corsheaders",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # DripFit apps
    "apps.accounts",
    "apps.wardrobe",
    "apps.outfits",
    "apps.analyser",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "dripfit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dripfit.wsgi.application"

# -------------------------------------------------------------------
# Database
# -------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL:
    import dj_database_url  # type: ignore
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -------------------------------------------------------------------
# Auth & allauth (Google OAuth)
# -------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
SOCIALACCOUNT_AUTO_SIGNUP = True
LOGIN_REDIRECT_URL = "http://localhost:5173/"
LOGOUT_REDIRECT_URL = "http://localhost:5173/"
ACCOUNT_LOGOUT_REDIRECT_URL = "http://localhost:5173/"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

# -------------------------------------------------------------------
# Django REST Framework
# -------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# -------------------------------------------------------------------
# CORS (allow React dev server)
# -------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True

# Session & CSRF cookies — allow cross-port (5173 → 8000) without HTTPS
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE   = False
CSRF_COOKIE_SAMESITE    = "Lax"
CSRF_COOKIE_SECURE      = False

# CSRF: trust the Vite dev server origin so OAuth POST succeeds
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# -------------------------------------------------------------------
# Media files (wardrobe uploads)
# -------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / os.getenv("MEDIA_ROOT", "media")

# -------------------------------------------------------------------
# Static files
# -------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# -------------------------------------------------------------------
# Hugging Face
# -------------------------------------------------------------------
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
HF_VISION_MODEL = os.getenv("HF_VISION_MODEL", "Salesforce/blip-image-captioning-large")

# -------------------------------------------------------------------
# Misc
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
