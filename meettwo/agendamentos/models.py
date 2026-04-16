from django.db import models

# Create your models here.

class tipos_de_servicos(models.Model):

    servico_nome = models.CharField(max_length=30, null=True)
    tempo_duracao = models.TimeField()



class horarios_agendados(models.Model):

    cliente = models.TextField( max_length= 30)
    horario_agendado_inicial = models.DateTimeField()
    horario_agendado_final = models.DateTimeField()
    servico = models.TextField( max_length= 30)
    #seria interesante ter o numero de telefone do usuario



class dias_inoperante(models.Model):

    dia_funcionando_inteiro = models.DateField() #nesses dias a empresa nao opera 



class dias_ocupado(models.Model): #nesse intervalo de tempo a empresa nao funciona

    dia_ocupado_metade_inicio = models.DateTimeField()
    dia_ocupado_metade_fim = models.DateTimeField()



class horario_de_funcionamento(models.Model):

    #esse é o horario que a loja funciona, fora desse horario nao aceita agendamentos 
    horario_de_funcionamento_inicio = models.TimeField(null=True)
    horario_de_funcionamento_fim = models.TimeField(null=True)


