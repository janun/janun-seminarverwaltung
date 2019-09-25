from django.views.generic import DetailView
from django.db.models import Sum

from .models import JANUNGroup


class JANUNGroupDetailView(DetailView):
    model = JANUNGroup
    template_name = "groups/group_detail.html"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seminars_next_year"] = self.object.seminars.next_year().order_by(
            "start_date"
        )
        context["stats_next_year"] = (
            context["seminars_next_year"]
            .is_not_rejected()
            .aggregate(tnt_sum=Sum("tnt"), funding_sum=Sum("funding"))
        )
        context["seminars_this_year"] = self.object.seminars.this_year().order_by(
            "start_date"
        )
        context["stats_this_year"] = (
            context["seminars_this_year"]
            .is_not_rejected()
            .aggregate(tnt_sum=Sum("tnt"), funding_sum=Sum("funding"))
        )
        context["seminars_last_year"] = self.object.seminars.last_year().order_by(
            "start_date"
        )
        context["stats_last_year"] = (
            context["seminars_last_year"]
            .is_not_rejected()
            .aggregate(tnt_sum=Sum("tnt"), funding_sum=Sum("funding"))
        )
        return context
