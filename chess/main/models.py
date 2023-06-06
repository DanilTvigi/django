from django.db import models
from django.conf import settings

class GameHistory(models.Model):
    pin_game = models.IntegerField(default=0, null=True, blank=True)
    user_W = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_id_W', on_delete=models.CASCADE)
    username_W = models.CharField(max_length=20)
    user_B = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_id_B', on_delete=models.CASCADE)
    username_B = models.CharField(max_length=20)
    result = models.CharField(max_length=10, null=True, blank=True)
    lenght_game = models.IntegerField(default=0, null=True, blank=True)
    dateTime = models.DateTimeField(null=True, blank=True)
