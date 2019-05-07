""" Production Settings """

import os

import dj_database_url

from .dev import *  # noqa: F401,F403 # pylint: disable=unused-wildcard-import,wildcard-import

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}


DEBUG = bool(os.getenv('DJANGO_DEBUG', ''))

# Set to your Domain here (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = ['*']
