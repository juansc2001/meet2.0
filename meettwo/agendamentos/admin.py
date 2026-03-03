from django.contrib import admin
from .models import tipos_de_servicos,dias_inoperante,horario_de_funcionamento,horarios_agendados,dias_ocupado
# Register your models here.


admin.site.register(tipos_de_servicos)
admin.site.register(dias_inoperante)
admin.site.register(horario_de_funcionamento)
admin.site.register(horarios_agendados)
admin.site.register(dias_ocupado)

