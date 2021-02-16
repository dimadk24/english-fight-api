"""
Django settings for enfight project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

import sentry_sdk
from environ import environ, ImproperlyConfigured
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
dotenv_file = BASE_DIR / ".env"
if dotenv_file.exists():
    environ.Env.read_env(str(dotenv_file))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool)

DEBUG_SQL_QUERIES = env("DEBUG_SQL_QUERIES", cast=bool)

ALLOWED_HOSTS = ["127.0.0.1", env("DEPLOY_HOST")] if not DEBUG else ["*"]

# Sentry

if not DEBUG:
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.5,
    )

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "debug_toolbar",
    "admin_honeypot",
    "game",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_cprofile_middleware.middleware.ProfilerMiddleware",
]

ROOT_URLCONF = "enfight.urls"

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

WSGI_APPLICATION = "enfight.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        **env.db(),
        "CONN_MAX_AGE": 28800,
        # Default MySQL connection timeout
        "TEST": {
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Minsk"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT", default=None)
STATICFILES_DIRS = [
    ("picture-questions", BASE_DIR / "data" / "static_pictures")
]

AUTH_USER_MODEL = "game.AppUser"

LOGIN_URL = "/admin/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

if not DEBUG:
    # SSL related settings not suitable for local environment
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # Prod is deployed at subdomain, thus cannot use preload
    SECURE_HSTS_PRELOAD = False

# Django CORS headers

CORS_ORIGIN_ALLOW_ALL = DEBUG

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "https://localhost:3000",
    env("UI_HOST"),
]

CORS_URLS_REGEX = r"^/api/.*$"

# Django rest framework

DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)
DEFAULT_AUTHENTICATION_CLASSES = (
    "rest_framework.authentication.SessionAuthentication",  # for admin
    "game.authentication_backends.vk_app_authentication.VKAppAuthentication",
)

if DEBUG:
    # Allow browsable api in dev mode
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )
    DEFAULT_AUTHENTICATION_CLASSES = DEFAULT_AUTHENTICATION_CLASSES + (
        "game.authentication_backends."
        "fake_vk_id_authentication.FakeVKIDAuthentication",
    )

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
}

# Django hashid field

HASHID_FIELD_SALT = env("HASHID_FIELD_SALT")

# VK

VK_SECRET = env("VK_SECRET")
VK_SERVICE_TOKEN = env("VK_SERVICE_TOKEN")
VK_API_VERSION = "5.126"
VK_ALLOWED_USERS = env.list("VK_ALLOWED_USERS")
if not len(VK_ALLOWED_USERS):
    raise ImproperlyConfigured(
        'You should define VK_ALLOWED_USERS either as "*" or '
        "as list of valid user VK ids"
    )
if not VK_ALLOWED_USERS[0] == "*":
    VK_ALLOWED_USERS = [int(vk_id) for vk_id in VK_ALLOWED_USERS]

# cProfile middleware

DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False

# Debug toolbar

INTERNAL_IPS = [
    "127.0.0.1",
]

# Logging

if DEBUG and DEBUG_SQL_QUERIES:
    LOGGING = {
        "version": 1,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django.db.backends": {
                "level": "DEBUG",
            },
        },
        "root": {
            "handlers": ["console"],
        },
    }

if not DEBUG:
    LOG_DIR = env("DJANGO_LOG_DIR", default=".")
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": os.path.join(LOG_DIR, "logging.log"),
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": env("DJANGO_LOG_LEVEL", default="INFO"),
                "propagate": True,
            },
        },
    }
