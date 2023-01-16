from djongo import models
from django.utils.crypto import get_random_string


class MatchStatus(models.Model):
    # CREAMOS LAS OPCIONES DEL STATUSTYPE
    START = 'STA'
    BREAK = 'BRE'
    RESUMPTION = 'RES'
    GOAL = 'GOA'
    END = 'END'
    OTHER = 'OTH'

    STATUS_OPTIONS = (
        (START, 'Start'),
        (BREAK, 'Break'),
        (RESUMPTION, 'Resumption'),
        (GOAL, 'Goal'),
        (END, 'End'),
        (OTHER, 'Other'),
    )

    id = models.CharField(primary_key=True, max_length=24, default=get_random_string(length=24))
    status_type = models.CharField(
        max_length=3,
        choices=STATUS_OPTIONS,
    )
    matchId = models.CharField(max_length=24)
    info = models.CharField(max_length=255)
    date = models.DateTimeField()
    scoreboard = models.CharField(max_length=255)

class Tweet(models.Model):
    id =  models.CharField(primary_key=True, max_length=24, default=get_random_string(length=24))
    minuto = models.IntegerField()
    local = models.CharField(max_length=255)
    visitante = models.CharField(max_length=255)
    marcador = models.CharField(max_length=255)
    info = models.CharField(max_length=1500)