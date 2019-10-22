from django.views.generic import TemplateView


class Dashboard(TemplateView):
    template_name = "dashboard/dashboard.html"
    seminar_limit = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["janun_groups"] = self.request.user.janun_groups.all()
        context["group_hats"] = self.request.user.group_hats.all()
        context["seminars"] = self.request.user.seminars.all().order_by("created_at")[
            : self.seminar_limit
        ]
        context["show_more_link"] = (
            self.request.user.seminars.count() > self.seminar_limit
        )
        return context
