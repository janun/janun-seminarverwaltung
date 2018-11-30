from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, user, form, commit=True):
        # print(form.cleaned_data) # missing username because form __init__ del
        user = super().save_user(request, user, form, commit=False)
        data = form.cleaned_data
        # user.username = data['username']
        user.name = data['name']
        # user.phone_number = data['phone_number']
        # user.address = data['address']
        if commit:
            user.save()
        user.janun_groups.set(data['janun_groups'])
        if commit:
            user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
