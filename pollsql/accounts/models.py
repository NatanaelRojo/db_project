import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# Domains
phone_number_patron = re.compile('[0-9]{11}')
identification_patron = re.compile('(V|J|E)(([0-9]|-)+)')

# Validators
def phone_number_validator(phone_number):
    if (not phone_number_patron.fullmatch(phone_number)):
        raise ValidationError('This phone number is not valid')

def identification_validator(identification):
    if (not identification_patron.fullmatch(identification)):
        raise ValidationError('This identification document is not valid')

class CustomUser(AbstractUser):
    identification = models.CharField(
        max_length=10,
        validators=[identification_validator],
        default='V000000000',
        )
    phone_number = models.CharField(
        max_length=11,
        default='00000000000',
        validators=[phone_number_validator]
        )
    creation_date = models.DateTimeField(
        'creation date',
        default=timezone.now()
        )

    def __str__(self):
        return self.username