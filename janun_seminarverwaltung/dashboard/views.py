from django.views.generic import TemplateView


class Dashboard(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        context['group_hats'] = user.group_hats.all()
        context['janun_groups'] = user.janun_groups.all()

        context['seminars'] = user.get_seminars()[:6]
        return context
