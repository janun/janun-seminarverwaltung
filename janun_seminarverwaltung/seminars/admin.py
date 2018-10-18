from django.contrib import admin

from fsm_admin.mixins import FSMTransitionMixin
from import_export import resources
from import_export.admin import ImportExportMixin

from .models import Seminar


class QuarterListFilter(admin.SimpleListFilter):
    title = "Quartal"
    parameter_name = 'quarter'

    def lookups(self, request, model_admin):
        return (
            ('1', "1. Quartal"),
            ('2', "2. Quartal"),
            ('3', "3. Quartal"),
            ('4', "4. Quartal"),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.by_quarter(int(self.value()))
        return queryset


class YearListFilter(admin.SimpleListFilter):
    title = "Jahr"
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        year_dates = qs.dates('start', 'year', order='DESC')
        return [(date.year, date.year) for date in year_dates]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.by_year(int(self.value()))
        return queryset


class SeminarResource(resources.ModelResource):
    class Meta:
        model = Seminar
        widgets = {
            'start_date': {'format': '%d.%m.%Y'},
            'end_date': {'format': '%d.%m.%Y'},
            'author': {'model': 'users.User', 'field': 'username'},
            'group': {'model': 'groups.JANUNGroup', 'field': 'name'},
        }


@admin.register(Seminar)
class SeminarAdmin(FSMTransitionMixin, ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'start_date', 'group', 'author', 'state', 'created')
    list_select_related = ('group', 'author')
    date_hierarchy = 'start_date'
    list_filter = (
        YearListFilter, QuarterListFilter, 'state', 'group', 'author',
    )
    actions = None
    empty_value_display = "-kein-"
    search_fields = ['title']
    autocomplete_fields = ['author', 'group']
    resource_class = SeminarResource
