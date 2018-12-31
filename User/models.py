from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.FileField(null=True)
    games_count = models.IntegerField(null=True)
    email = models.EmailField()
    average_game_score = models.FloatField(null=True)
    average_user_score = models.FloatField(null=True)
    birth_date = models.DateField()
    sex = models.BooleanField()  # true -> male, false -> female
    password = models.CharField(max_length=30)
