from django.urls import path
from .views import log, cadastro
urlpatterns = [
    path('login/', log, name='login'),
    path('cadastro/', cadastro , name='cadastrar' ),
]