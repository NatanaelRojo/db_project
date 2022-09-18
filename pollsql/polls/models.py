import datetime
from django.db import models
from django.utils import timezone

from accounts.models import CustomUser

class Poll(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    image = models.ImageField(
        default='',
        null=True,
        blank=True
    )
    creation_date = models.DateTimeField(
        'date creation'
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.creation_date <= now

    def __str__(self):
        return self.name


class Question(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=200
    )
    creation_date = models.DateTimeField(
        'date creation'
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=200
    )
    votes = models.IntegerField(
        default=0
    )
    creation_date = models.DateTimeField(
        'date creation'
    )

