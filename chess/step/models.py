from django.db import models

class Desk(models.Model):
    name = models.CharField(max_length=15)
    ip = models.CharField(max_length=15)
    user = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=20)

class Steps(models.Model):
    pin_game = models.IntegerField()
    queue_step = models.IntegerField()
    user_id_W = models.IntegerField(default=5)
    user_id_B = models.IntegerField(default=5)
    step = models.CharField(max_length=10)
    time = models.DateTimeField()
