from django.db import models

# Create your models here.

class MatchStatus(models.Model):
    #TENEMOS QUE CREAR EL TIPO STATUS PERO SUBO ASÍ DE MOMENTO PARA SEGUIR TRABAJANDO
    statusType = models.CharField(max_length=255)
    info = models.CharField(max_length=255)
    date = models.DateTimeField()
    scoreboard = models.CharField(max_length=255)
    uidPlayer = models.CharField(max_length=255)
