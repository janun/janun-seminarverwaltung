from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from templated_email import send_templated_mail

from janun_seminarverwaltung.users.models import get_verwalter_mails
from context_processors import janun_context


def send_seminar_mail(template_name, emails, seminar, request):
    if not isinstance(emails, (list, tuple)):
        emails = [emails]
    context = janun_context(request)
    context.update({
        'seminar': seminar,
        'user': request.user,
        'seminar_url': request.build_absolute_uri(seminar.get_absolute_url()),
        'current_site': get_current_site(request)
    })
    send_templated_mail(
        template_name=template_name,
        from_email=settings.DEFAULT_FROM_EMAIL,
        headers=settings.DEFAULT_EMAIL_HEADERS,
        recipient_list=emails,
        context=context
    )
