from django.conf import settings
from django.template import TemplateDoesNotExist

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from templated_email import send_templated_mail

from context_processors import janun_context


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        data = form.cleaned_data
        user.name = data['name']
        user.phone_number = data['phone_number']
        # user.address = data['address']
        if commit:
            user.save()
        user.janun_groups.set(data['janun_groups'])
        if commit:
            user.save()
        return user

    def send_mail(self, template_prefix, email, context):
        context.update(janun_context(None))
        try:
            send_templated_mail(
                template_name=template_prefix.split('/')[-1],
                from_email=settings.DEFAULT_FROM_EMAIL,
                headers=settings.DEFAULT_EMAIL_HEADERS,
                recipient_list=[email],
                context=context
            )
        except TemplateDoesNotExist:
            super().send_mail(template_prefix, email, context)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
