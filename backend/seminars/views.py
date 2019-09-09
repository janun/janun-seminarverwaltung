from django.views.generic.list import ListView
from .models import Seminar


class SeminarListView(ListView):
    model = Seminar
    template_name = "seminars/seminar_list.html"
