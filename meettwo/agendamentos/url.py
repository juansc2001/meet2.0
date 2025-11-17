from django.urls import path
from .views import home_page, servicos

urlpatterns = [
    path('', home_page, name= 'home'),
    path('servicos/', servicos, name= 'servico_adm')
]