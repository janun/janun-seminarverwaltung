from django.conf import settings


def janun_context(request):
    return {
        'SEMINAR_POLICY_URL': settings.SEMINAR_POLICY_URL,
        'HELP_PHONE': settings.HELP_PHONE,
        'HELP_EMAIL': settings.HELP_EMAIL,
        'HELP_PHONE_LINK': settings.HELP_PHONE_LINK,
    }
