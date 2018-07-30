from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


def dispatch_by_user(verwalter_view, pruefer_view, teamer_view):
    def get_view(request, **kwargs):
        if request.user.role == "VERWALTER":
            return verwalter_view(request, **kwargs)
        if request.user.role == "PRUEFER":
            return pruefer_view(request, **kwargs)
        if request.user.role == "TEAMER":
            return teamer_view(request, **kwargs)
    return get_view
