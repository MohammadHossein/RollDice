from django.contrib.auth.models import User as djangoUser
from django.db import models


# Create your models here.


class User(djangoUser):
    photo = models.FileField(null=True)
    games_count = models.IntegerField(null=True,default=0)
    average_game_score = models.FloatField(null=True,default=0)
    average_user_score = models.FloatField(null=True,default=0)
    birth_date = models.DateField()
    sex = models.BooleanField()  # true -> male, false -> female
    isAdmin = models.BooleanField(default=False)
