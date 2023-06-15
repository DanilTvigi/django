# from django.conf import settings
# from django.db import models
# from django.contrib.auth.models import AbstractUser, User


# class CustomUser(AbstractUser):
#     play_count = models.IntegerField(null=True, default=0)
#     win = models.IntegerField(null=True, default=0)
#     lose = models.IntegerField(null=True, default=0)
#     minuteInGame = models.IntegerField(null=True, default=0)
#     rating = models.FloatField(null=True, default=0)
#     groups = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='customuser_groups', blank=True)
#     user_permissions = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='customuser_user_permissions', blank=True)



# class SessionConnection(models.Model):
#     user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='session_connections1', on_delete=models.CASCADE)
#     user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='session_connections2', on_delete=models.CASCADE, null=True)
#     pin_game = models.CharField(max_length=6)
#     desk = models.IntegerField()
#     min = models.CharField(max_length=3)
#     delete_time = models.DateTimeField(null=True, blank=True)
#     cords_ancle = models.CharField(max_length=200)   


from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User


class CustomUser(AbstractUser):
    play_count = models.IntegerField(null=True, default=0)
    win = models.IntegerField(null=True, default=0)
    lose = models.IntegerField(null=True, default=0)
    minuteInGame = models.IntegerField(null=True, default=0)
    rating = models.FloatField()
    
    groups = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='customuser_user_permissions', blank=True)



class SessionConnection(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='session_connections1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='session_connections2', on_delete=models.CASCADE, null=True)
    pin_game = models.CharField(max_length=6)
    desk = models.IntegerField()
    min = models.CharField(max_length=3)
    # sec = models.CharField(max_length=2)
    delete_time = models.DateTimeField(null=True, blank=True)
    cords_ancle = models.CharField(max_length=200)   







