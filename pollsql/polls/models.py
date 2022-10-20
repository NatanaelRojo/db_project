import datetime
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import CustomUser

# Domains
only_characters_patron = re.compile('([a-z]|[A-Z]|[0-9]|(\s+))+')
question_patron = re.compile('¿([a-z]|[A-Z]|[0-9]|(\s+))+\?')

# Validators
def only_characters_validator(characters):
    if (not only_characters_patron.fullmatch(characters)):
        raise ValidationError('This text is not valid')

def question_validator(question):
    if (not question_patron.fullmatch(question)):
        raise ValidationError('This question is not valid')
        

class Poll(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100,
        validators=[only_characters_validator],
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        validators=[only_characters_validator],
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
        max_length=200,
        validators=[question_validator],
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
        max_length=200,
        validators=[only_characters_validator],
    )
    votes = models.IntegerField(
        default=0
    )
    creation_date = models.DateTimeField(
        'date creation'
    )

