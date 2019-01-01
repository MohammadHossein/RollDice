from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from User.models import User


class Game(models.Model):
    rate = models.FloatField(default=0)
    creation_date = models.DateTimeField(auto_now=True)
    max_score = models.IntegerField(default=0)
    dice_count = models.IntegerField(default=1)
    hold = models.CharField(max_length=100)
    max_roll = models.IntegerField(default=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='createdBy')
    play_count = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    
