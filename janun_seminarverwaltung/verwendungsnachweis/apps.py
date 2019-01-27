from django.apps import AppConfig


class VerwendungsnachweisConfig(AppConfig):
    name = "janun_seminarverwaltung.verwendungsnachweis"
    verbose_name = "Verwendungsnachweis"

    def ready(self):
        """Override this to put in:
            Verwendungsnachweis system checks
            Verwendungsnachweis signal registration
        """
        try:
            import verwendungsnachweis.signals  # noqa F401
        except ImportError:
            pass
