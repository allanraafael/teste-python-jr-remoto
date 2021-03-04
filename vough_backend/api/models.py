from django.db import models


class Organization(models.Model):
    login = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, default="")
    score = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.login} - score:{self.score}'
