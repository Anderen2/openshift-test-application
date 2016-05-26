from django.db import models

# Create your models here.

class MessageModel(models.Model):
    username = models.CharField(max_length=32)
    room_id = models.IntegerField()
    datetime = models.DateTimeField()
    content = models.TextField()
    rating = models.TextField()
    device_type = models.CharField(max_length=32)

class UserModel(models.Model):
    username = models.CharField(max_length=32)
    avatar = models.CharField(max_length=32)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=256)

class RoomModel(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=1024)
