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
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "simple_history",
    "django_filters",
    "django_tables2",
    "djcelery_email",
    "preferences",
    "phonenumber_field",
    "crispy_forms",
    "import_export",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_admin_listfilter_dropdown",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "allauth_2fa",
]
LOCAL_APPS = [
    "backend.seminars.apps.SeminarsConfig",
    "backend.users.apps.UsersConfig",
    "backend.groups.apps.GroupsConfig",
    "backend.dashboard.apps.DashboardConfig",
    "backend.emails.apps.EmailsConfig",
    "backend.config.apps.ConfigConfig",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# MIGRATION_MODULES = {}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "dashboard:dashboard"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

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
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "backend.validators.PwnedPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "allauth_2fa.middleware.AllauthTwoFactorMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "backend.users.middleware.SetLastVisitMiddleware",
    "backend.users.middleware.RequireLoginMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR.path("static")), str(ROOT_DIR.path("node_modules"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(APPS_DIR("media"))
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APPS_DIR.path("templates")],
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
                "preferences.context_processors.preferences_cp",
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
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = env(
    "CELERY_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
# ADMIN_URL = r"^admin/"
ADMINS = [("Henrik Kroeger", "hedwig@janun.de")]
MANAGERS = ADMINS


# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ADAPTER = "backend.users.forms.AccountAdapter"
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_FORMS = {
    "signup": "backend.users.forms.SignupForm",
    "change_password": "backend.users.forms.ChangePasswordForm",
    "login": "backend.users.forms.LoginForm",
}
ACCOUNT_LOGOUT_REDIRECT_URL = "account_login"
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 600
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

# Your stuff...
# ------------------------------------------------------------------------------
CRISPY_TEMPLATE_PACK = "janunforms"
CRISPY_ALLOWED_TEMPLATE_PACKS = ("janunforms",)

LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r"^/accounts/login/$",
    r"^/accounts/logout/$",
    r"^/accounts/signup/$",
    r"^/accounts/password/reset/$",
    r"^/accounts/password/reset/done/$",
    r"^/accounts/password/reset/key/(.*)$",
    r"^/accounts/password/reset/key/done/$",
    r"^/accounts/two-factor-authenticate$",
)


# phonenumber
PHONENUMBER_DEFAULT_REGION = "DE"


# CELERY STUFF
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379")
CELERY_RESULT_BACKEND = env("REDIS_URL", default="redis://localhost:6379")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/Berlin"

# Simple history
SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True


TIME_INPUT_FORMATS = [
    "%H:%M",  # 14:30
    "%H:%M:%S",  # 14:30:59
    "%H:%M:%S.%f",  # 14:30:59.000200
    "%H.%M",  # 14.30
    "%H.%M Uhr",  # 14.30 Uhr
    "%H.%M h",  # 14.30 h
    "%H.%MUhr",  # 14.30Uhr
    "%H.%Mh",  # 14.30h
    "%H Uhr",  # 14Uhr
    "%HUhr",  # 14Uhr
]
