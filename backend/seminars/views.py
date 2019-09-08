from django_filters.views import FilterView
from .models import Seminar
from .filters import SeminarFilter


class SeminarListView(FilterView):
    model = Seminar
    filterset_class = SeminarFilter
    template_name = "seminars/seminar_list.html"
