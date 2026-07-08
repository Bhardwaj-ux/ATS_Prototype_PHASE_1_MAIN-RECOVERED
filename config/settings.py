import os
from pathlib import Path

import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


ON_VERCEL = bool(os.getenv("VERCEL")) or bool(os.getenv("VERCEL_ENV"))

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-phase1-local-dev-key")
DEBUG = env_bool("DEBUG", default=not ON_VERCEL)

if ON_VERCEL and SECRET_KEY == "django-insecure-phase1-local-dev-key":
    raise RuntimeError("SECRET_KEY must be set on Vercel.")

vercel_url = os.getenv("VERCEL_URL", "").strip()
extra_hosts = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()]

allowed_hosts = ["127.0.0.1", "localhost", ".vercel.app"]
if vercel_url:
    allowed_hosts.append(vercel_url)
allowed_hosts.extend(extra_hosts)
ALLOWED_HOSTS = list(dict.fromkeys(allowed_hosts))

app_url = os.getenv("APP_URL", "").strip().rstrip("/")
extra_origins = [origin.strip().rstrip("/") for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin.strip()]

csrf_trusted_origins = []
if app_url:
    csrf_trusted_origins.append(app_url)
if vercel_url:
    csrf_trusted_origins.append(f"https://{vercel_url}")
csrf_trusted_origins.extend(extra_origins)
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(csrf_trusted_origins))


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.core",
    "apps.accounts",
    "apps.jobs",
    "apps.applications",
    "apps.resumes",
    "apps.dashboard",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.accounts.context_processors.user_preferences",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"
# ASGI_APPLICATION = "config.asgi.application"


database_url = os.getenv("DATABASE_URL", "").strip()

if ON_VERCEL and not database_url:
    raise RuntimeError(
        "DATABASE_URL is required on Vercel. SQLite becomes read-only there and breaks login/session writes."
    )

if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "dashboard:index"
LOGOUT_REDIRECT_URL = "accounts:login"


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
