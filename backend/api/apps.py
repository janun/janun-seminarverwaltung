from django.apps import AppConfig as OrigAppConfig


class AppConfig(OrigAppConfig):
    name = 'api'
