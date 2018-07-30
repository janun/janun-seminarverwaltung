from django.views.generic import TemplateView

from seminars.models import Seminar


class VerwalterDashboard(TemplateView):
    template_name = "dashboard/verwalter_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seminars'] = Seminar.objects.order_by('-created').all()[:3]
        return context


class PrueferDashboard(TemplateView):
    template_name = "dashboard/pruefer_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = self.request.user.group_hats.all()
        context['seminars'] = Seminar.objects.filter(
            group__in=self.request.user.group_hats.all()
        )[:3]
        return context


class TeamerDashboard(TemplateView):
    template_name = "dashboard/teamer_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = self.request.user.janun_groups.all()
        context['seminars'] = Seminar.objects.filter(author=self.request.user)[:3]
        return context
