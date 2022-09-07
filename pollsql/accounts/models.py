from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    #identification = models.CharField(max_length=200)
    email = models.CharField(
        max_length=254,
        unique=True
    )
    #phone_number = models.CharField(max_length=11)
    #creation_date = models.DateTimeField('creation date')

    def __str__(self):
        return self.username