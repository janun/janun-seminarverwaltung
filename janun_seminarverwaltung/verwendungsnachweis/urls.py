from django.urls import path
from .views import VWNIndexView, VWNUebersichtView, VWNDeckblatterView

app_name = 'verwendungsnachweis'

urlpatterns = [
    path('', VWNIndexView.as_view(), name='index'),
    path('<int:year>/uebersicht', VWNUebersichtView.as_view(), name='uebersicht'),
    path('<int:year>/deckblaetter', VWNDeckblatterView.as_view(), name='deckblaetter'),
]
