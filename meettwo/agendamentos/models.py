from django.db import models

# Create your models here.

class tipos_de_servicos(models.Model):

    servico_nome = models.CharField(max_length=30, null=True)
    tempo_duracao = models.TimeField()



