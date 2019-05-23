"""
Base settings to build other settings files upon.
"""

import environ

ROOT_DIR = environ.Path(__file__) - 3  # = janun-seminarverwaltung/)
APPS_DIR = ROOT_DIR.path("backend")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "Europe/Berlin"
LANGUAGE_CODE = "de-de"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DATABASES
# ------------------------------------------------------------------------------

DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]
THIRD_PARTY_APPS = [
    "django_filters",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "rest_auth.registration",
    "corsheaders",
]
LOCAL_APPS = ["backend.api"]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# MIGRATION_MODULES = {}

# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "api.User"

# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
        "OPTIONS": {"user_attributes": ("username", "name", "email")},
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    # {"NAME": "janun_seminarverwaltung.validators.PwnedPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "backend.api.middleware.SetLastVisitMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# Not really using staticfiles, since only serving an api
STATIC_ROOT = str(ROOT_DIR("dist"))
STATIC_URL = "/static/"
STATICFILES_DIRS = []
STATICFILES_FINDERS = []


# WhiteNoise
# ------------------------------------------------------------------------------
# Serve frontend files with whitenoise
WHITENOISE_INDEX_FILE = True
WHITENOISE_ROOT = ROOT_DIR("dist")


# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(APPS_DIR("media"))
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ROOT_DIR("dist")],
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = r"^admin/"
ADMINS = [("Henrik Kroeger", "hedwig@janun.de")]
MANAGERS = ADMINS


# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False


# django-cors
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = [r"^http://localhost:.*$"]
CORS_URLS_REGEX = r"^/api/.*$"


# django-restframework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAdminUser",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
}

REST_FRAMEWORK_EXTENSIONS = {
    "DEFAULT_OBJECT_CACHE_KEY_FUNC": (
        "backend.api.key_constructors.CustomObjectKeyFunction"
    ),
    "DEFAULT_LIST_CACHE_KEY_FUNC": "backend.api.key_constructors.CustomListKeyFunction",
    "DEFAULT_OBJECT_ETAG_FUNC": "backend.api.key_constructors.CustomObjectKeyFunction",
    "DEFAULT_LIST_ETAG_FUNC": "backend.api.key_constructors.CustomListKeyFunction",
}

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "backend.api.serializers.UserProfileSerializer"
}
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "backend.api.serializers.RegisterSerializer"
}
REST_SESSION_LOGIN = False


# Your stuff...
# ------------------------------------------------------------------------------
