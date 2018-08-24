from django.core import mail
from django.template.loader import render_to_string

from janun_seminarverwaltung.users.models import User


# TODO: move to models and what about group_hat for einzelpersonen?
def get_verwalter_and_pruefer_mails(group):
    qs = User.objects.filter(role='VERWALTER')
    qs |= User.objects.filter(role='PRUEFER').filter(group_hats=group)
    return list(qs.values_list('email', flat=True))


def send_wizard_done_mails(seminar, request):
    with mail.get_connection(fail_silently=True) as connection:
        mail.EmailMessage(
            subject='Dein Seminar "{0}"'.format(seminar.title),
            body=render_to_string(
                'seminars/email/wizard_done_author.txt', {
                    'seminar': seminar,
                    'user': seminar.author,
                    'seminar_url': request.build_absolute_uri(seminar.get_absolute_url())
                    }),
            from_email='website@janun.de',
            to=[seminar.author.email],
            reply_to=['seminare@janun.de'],
            connection=connection
        ).send()
        mail.EmailMessage(
            subject='Neues Seminar "{0}"'.format(seminar.title),
            body=render_to_string(
                'seminars/email/wizard_done_verwalter.txt', {
                    'seminar': seminar,
                    'user': seminar.author,
                    'seminar_url': request.build_absolute_uri(seminar.get_absolute_url())
                    }),
            from_email='website@janun.de',
            to=get_verwalter_and_pruefer_mails(seminar.group),
            reply_to=['seminare@janun.de'],
            connection=connection
        ).send()
