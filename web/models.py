from django.db import models

# Create your models here.


class MessageModel(models.Model):
    user_id = models.ForeignKey(
        'UserModel',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    room_id = models.ForeignKey(
        'RoomModel',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    datetime = models.DateTimeField()
    content = models.TextField()
    rating = models.TextField() # If I gave you a nickle, would you tickle my pickle?

class UserModel(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=256)

class RoomModel(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=1024)
