from django.urls import path
from .views import home_page, servicos, agendar, dia_disponivel

urlpatterns = [
    path('', home_page, name= 'home'),
    path('servicos/', servicos, name= 'servico_adm'),
    path('agendar_reuniao/', agendar, name='agendar_form'),
    path('dia_disponivel/', dia_disponivel, name='disponibilidade')
]