from django.db import models

# Create your models here.

class MatchStatus(models.Model):
    #CREAMOS LAS OPCIONES DEL STATUSTYPE
    START = 'STA'
    BREAK = 'BRE'
    RESUMPTION = 'RES'
    GOAL = 'GOA'
    END = 'END'
    OTHER = 'OTH'

    STATUS_OPTIONS = (
        (START, 'Start'),
        (BREAK, 'Break'),
        (RESUMPTION, 'Resumotion'),
        (GOAL, 'Goal'),
        (END, 'End'),
        (OTHER, 'Other'),
    )
    
    statusType = models.CharField(
        max_length=3,
        choices=STATUS_OPTIONS,
    )
    info = models.CharField(max_length=255)
    date = models.DateTimeField()
    scoreboard = models.CharField(max_length=255)
    uidPlayer = models.CharField(max_length=255)
