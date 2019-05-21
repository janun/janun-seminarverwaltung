"""
With these settings, tests run faster.
"""

from .base import *  # noqa pylint: disable=wildcard-import, unused-wildcard-import
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = False
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="4y70dAx0LNwE8LIz9QE959sgLAkUvU6lmOuQ9ckElW4COMqC7tmbKCS7bIcDM7iN",
)
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  # noqa F405
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

# Your stuff...
# ------------------------------------------------------------------------------
