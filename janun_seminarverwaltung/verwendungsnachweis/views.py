from django.shortcuts import render
from django.views import View

from seminars.models import Seminar

from verwendungsnachweis.templateddocs import fill_template, FileResponse


class Verwendungsnachweis:
    def __init__(self, year, seminars):
        self.year = year
        self.seminars = seminars

    def count(self):
        return self.seminars.count()


class VWNIndexView(View):
    template_name = 'verwendungsnachweis/index.html'

    def get(self, request, *args, **kwargs):
        years = [o.year for o in Seminar.objects.distinct().order_by('start_date').dates('start_date', 'year', order='DESC')]
        object_list = []
        for year in years:
            object_list.append(Verwendungsnachweis(
                year=year,
                # TODO Filter Seminars
                seminars=Seminar.objects.filter(start_date__year=year)
            ))
        return render(request, self.template_name, {'object_list': object_list})


class VWNUebersichtView(View):
    pass


class VWNDeckblatterView(View):
    def get(self, request, *args, **kwargs):
        year = kwargs['year']
        context = {
            'seminars': Seminar.objects.filter(start_date__year=year)
        }
        filename = fill_template('verwendungsnachweis/deckblatt.odt', context)
        visible_filename = 'Verwendungsnachweis {} Deckblätter.odt'.format(year)
        return FileResponse(filename, visible_filename)
