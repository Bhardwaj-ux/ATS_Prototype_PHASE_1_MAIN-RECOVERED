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
extra_hosts = [
    host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()
]

allowed_hosts = ["127.0.0.1", "localhost", ".vercel.app"]
if vercel_url:
    allowed_hosts.append(vercel_url)
allowed_hosts.extend(extra_hosts)
ALLOWED_HOSTS = list(dict.fromkeys(allowed_hosts))

app_url = os.getenv("APP_URL", "").strip().rstrip("/")
extra_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

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
    "storages",
    "rest_framework",
    "apps.core",
    "apps.accounts",
    "apps.jobs",
    "apps.jdimport",
    "apps.applications",
    "apps.resumes",
    "apps.dashboard",
    "apps.tasks",
    "apps.folks",
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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

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

# JS needs to read this cookie to send it back as a header on POST/PUT/DELETE
CSRF_COOKIE_HTTPONLY = False
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"

WSGI_APPLICATION = "config.wsgi.application"
# ASGI_APPLICATION = "config.asgi.application"


database_url = os.getenv("DATABASE_URL", "").strip()

if ON_VERCEL and not database_url:
    raise RuntimeError(
        "DATABASE_URL is required on Vercel. SQLite becomes read-only there and breaks login/session writes."
    )

# Supabase's pooled connection string (pgbouncer, transaction mode — the one
# meant for serverless) doesn't support long-lived connections or server-side
# cursors. conn_max_age defaults to 0 so each request opens/closes cleanly
# against the pooler; override with DB_CONN_MAX_AGE if you switch to the
# direct (non-pooled) connection string instead.
DB_CONN_MAX_AGE = int(os.getenv("DB_CONN_MAX_AGE", "0"))

if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=DB_CONN_MAX_AGE,
            ssl_require=not DEBUG,
        )
    }
    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True
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

# Supabase Storage is S3-compatible, so it's accessed via django-storages'
# S3 backend rather than a Supabase-specific package. Two "folders" (prefixes)
# are used inside a single bucket: static/ and media/.
AWS_ACCESS_KEY_ID = os.environ.get("SUPABASE_S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("SUPABASE_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("SUPABASE_S3_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.environ.get(
    "SUPABASE_S3_ENDPOINT_URL"
)  # https://<project-ref>.supabase.co/storage/v1/s3
AWS_S3_REGION_NAME = os.environ.get("SUPABASE_S3_REGION", "ap-south-1")
AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

if ON_VERCEL and not all(
    [
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_STORAGE_BUCKET_NAME,
        AWS_S3_ENDPOINT_URL,
    ]
):
    raise RuntimeError(
        "SUPABASE_S3_ACCESS_KEY_ID, SUPABASE_S3_SECRET_ACCESS_KEY, SUPABASE_S3_BUCKET_NAME "
        "and SUPABASE_S3_ENDPOINT_URL are all required on Vercel."
    )

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {"location": "media"},
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {"location": "static"},
    },
}


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
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
