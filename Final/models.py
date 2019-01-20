import random
import string

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from User.models import User


class Game(models.Model):
    name = models.CharField(max_length=100, default='')
    rate = models.FloatField(default=0)
    rate_person_count = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now=True)
    max_score = models.IntegerField(default=0)
    dice_count = models.IntegerField(default=1)
    hold = models.CharField(max_length=100)
    max_roll = models.IntegerField(default=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='createdBy')
    play_count = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    average_score_person_count = models.IntegerField(default=0)


class GameComment(models.Model):
    text = models.TextField(default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userCommentGame')
    accept = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gameComment')
    rate = models.FloatField(default=0)


class UserComment(models.Model):
    text = models.TextField(default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userCommentUser')
    accept = models.BooleanField(default=False)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userComment')
    rate = models.FloatField(default=0)


class GameData:
    def __init__(self, dice_count, max_score, hold):
        self.id = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32))
        self.dices = []
        self.dice_count = dice_count
        self.turn = False
        self.max_score = max_score
        self.player1_current = 0
        self.player1_total = 0
        self.player2_current = 0
        self.player2_total = 0
        self.winner = None
        self.hold = hold
        self.player1_id = ''
        self.player2_id = ''
        self.started = False
