from django.contrib.auth.models import User as djangoUser
from django.db import models

# Create your models here.


class User(djangoUser):
    photo = models.FileField(null=True)
    games_count = models.IntegerField(null=True, default=0)
    average_game_score = models.FloatField(null=True, default=0)
    average_game_score_count = models.IntegerField(default=0)
    birth_date = models.DateField()
    sex = models.BooleanField()  # true -> male, false -> female
    isAdmin = models.BooleanField(default=False)

    @property
    def average_rate(self):
        from Final.models import UserComment
        my_comments = UserComment.objects.filter(to_user=self.id)
        return sum([x.rate for x in my_comments])/len(my_comments)
