"""
Django settings for watchmate project.
"""

import os
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security / environment ---
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-$*(4s7evu!!i0=3o#g1gqyf^60vqpveyw)e=+y%k(k51qe*+z(",
)

# DEBUG: False on PythonAnywhere (set in WSGI), True locally by default
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

# Host/CSRF: allow your PA domain + local
ALLOWED_HOSTS = [
    "marwan25.pythonanywhere.com",
    os.environ.get("PA_HOST", ""),
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://marwan25.pythonanywhere.com",
]

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "watchlist_app",

    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "watchmate.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "watchmate.wsgi.application"

# --- Database (SQLite for now) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Password validators ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- I18N ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --- Static files ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # for collectstatic on PA

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Django REST Framework ---
REST_FRAMEWORK = {
    # Permissions: leave open by default; tighten per-view as needed
    # "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],

    # Auth: keep TokenAuthentication (your current code); JWT optional below
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],

    # Throttling (your original values)
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "100/day",
        "review-create": "2/day",
        "review-list": "100/day",
        "review-detail": "100/day",
    },

    # Filters / search / ordering (added for API features)
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],

    # Pagination (page-number, size 10)
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,

    # Renderers (JSON-only like you had)
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

# Optional JWT settings (only used if you enable the auth class above)
# SIMPLE_JWT = {
#     "ROTATE_REFRESH_TOKENS": True,
#     # You can also set token lifetimes here if you switch to JWT later.
# }
