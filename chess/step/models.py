# from django.db import models

# class Desk(models.Model):
#     name = models.CharField(max_length=15)
#     ip = models.CharField(max_length=15)
#     user = models.CharField(max_length=15)
#     password = models.CharField(max_length=128)
#     status = models.CharField(max_length=20)


# # class Games(models.Model):
# #     user_id_W = models.IntegerField(default=5)
# #     username_W = models.CharField(max_length=25)
# #     user_id_B = models.IntegerField(default=5)
# #     username_B = models.CharField(max_length=25)
# #     result = models.CharField(max_length=5)
# #     length_game = models.IntegerField(default=0)
# #     dateTime = models.DateTimeField()

# class Steps(models.Model):
#     pin_game = models.IntegerField()
#     queue_step = models.IntegerField()
#     user_id_W = models.IntegerField(default=5)
#     user_id_B = models.IntegerField(default=5)
#     step = models.CharField(max_length=10)
#     time = models.DateTimeField()


from django.db import models

class Desk(models.Model):
    name = models.CharField(max_length=15)
    ip = models.CharField(max_length=15)
    user = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=20)


# class Games(models.Model):
#     user_id_W = models.IntegerField(default=5)
#     username_W = models.CharField(max_length=25)
#     user_id_B = models.IntegerField(default=5)
#     username_B = models.CharField(max_length=25)
#     result = models.CharField(max_length=5)
#     length_game = models.IntegerField(default=0)
#     dateTime = models.DateTimeField()

class Steps(models.Model):
    pin_game = models.IntegerField()
    queue_step = models.IntegerField()
    moves = models.TextField(max_length=200)
    user_id_W = models.IntegerField(default=5)
    user_id_B = models.IntegerField(default=5)
    step = models.CharField(max_length=10)
    time = models.DateTimeField()