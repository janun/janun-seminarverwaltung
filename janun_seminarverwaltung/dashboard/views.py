from django.views.generic import TemplateView
from janun_seminarverwaltung.users.models import User


class Dashboard(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        context['group_hats'] = user.group_hats.all()
        context['janun_groups'] = user.janun_groups.all()

        context['seminars'] = user.get_seminars()[:6]

        if self.request.user.role == 'VERWALTER':
            context['users_to_review'] = User.objects.filter(is_reviewed=False)

        return context
