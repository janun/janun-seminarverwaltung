from django.db import models
from django.views.generic import TemplateView

from janun_seminarverwaltung.users.models import User
from groups.models import JANUNGroup
from seminars.models import Seminar
# from seminars.stats import SeminarStats


class StaffDashboard(TemplateView):
    template_name = 'dashboard/staff_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'VERWALTER':
            context['all_seminars'] = Seminar.objects.order_by('-created').all()[:6]
            context['users_to_review'] = User.objects.filter(is_reviewed=False)
            context['groups_without_contacts'] = JANUNGroup.objects \
                .annotate(contact_count=models.Count("contact_people")) \
                .filter(contact_count__lt=3)
        return context


class TeamerDashboard(TemplateView):
    template_name = 'dashboard/teamer_dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['my_seminars'] = user.seminars.order_by('-created').all()[:6]
        context['my_seminars_count'] = user.seminars.count()
        return context


# class Dashboard(TemplateView):
#     template_name = 'dashboard/dashboard.html'
#
#     def get_context_data(self, **kwargs):
#         user = self.request.user
#         context = super().get_context_data(**kwargs)
#
#         context['group_hats'] = user.group_hats.all()
#         context['janun_groups'] = user.janun_groups.all()
#
#         # context['seminars'] = user.get_seminars()[:6]
#         context['my_seminars'] = user.seminars.order_by('-created').all()[:6]
#         context['my_seminars_count'] = user.seminars.count()
#
#         if self.request.user.role == 'VERWALTER':
#             context['all_seminars'] = Seminar.objects.order_by('-created').all()[:6]
#             context['users_to_review'] = User.objects.filter(is_reviewed=False)
#             context['groups_without_contacts'] = JANUNGroup.objects \
#                 .annotate(contact_count=models.Count("contact_people")) \
#                 .filter(contact_count__lt=3)
#
#         if user.has_perm('seminars.see_stats'):
#             context['seminar_stats'] = SeminarStats(Seminar.objects.all())
#
#         return context
