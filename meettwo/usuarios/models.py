from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class private_user_info(models.Model):

    #https://docs.djangoproject.com/en/5.2/ref/models/fields/ (models.Fields)
    usuario = models.ForeignKey( User, on_delete=models.CASCADE)
    telefone = models.IntegerField(blank=False)