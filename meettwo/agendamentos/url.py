from django.urls import path
from .views import home_page, servicos, agendar

urlpatterns = [
    path('', home_page, name= 'home'),
    path('servicos/', servicos, name= 'servico_adm'),
    path('agendar_reuniao/', agendar, name='agendar_form'),
]