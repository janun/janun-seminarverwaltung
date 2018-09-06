import django_filters

from seminars.models import Seminar
from groups.models import JANUNGroup
from janun_seminarverwaltung.users.models import User


class YearFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        kwargs['lookup_expr'] = "year"
        super().__init__(*args, **kwargs)

    @property
    def field(self):
        qs = self.model._default_manager.distinct()
        qs = qs.order_by(self.field_name).dates(self.field_name, 'year')
        self.extra['choices'] = [(o.year, o.year) for o in qs]
        return super().field


def allowed_groups(request):
    if request is None:
        return JANUNGroup.objects.none()
    user = request.user
    if user.role == 'VERWALTER':
        return JANUNGroup.objects.all()
    if user.role == 'PRUEFER':
        return user.group_hats.all()
    return user.janun_groups.all()


def allowed_users(request):
    if request is None:
        return User.objects.none()
    user = request.user
    if user.role in ('VERWALTER', 'PRUEFER'):
        return User.objects.all()
    return User.objects.filter(pk=user.pk)


class SeminarFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label="Titel", lookup_expr='icontains')
    start_year = YearFilter(label="Jahr", field_name="start")
    start_quarter = django_filters.ChoiceFilter(
        label="Quartal", field_name="start", lookup_expr='quarter',
        choices=[(i, "{0}. Quartal".format(i)) for i in range(1, 5)]
    )
    group = django_filters.ModelChoiceFilter(
        null_label='-- keine --', queryset=allowed_groups
    )
    author = django_filters.ModelChoiceFilter(
        queryset=allowed_users
    )

    class Meta:
        model = Seminar
        fields = ['title', 'start_year', 'start_quarter', 'group', 'author', 'state']
