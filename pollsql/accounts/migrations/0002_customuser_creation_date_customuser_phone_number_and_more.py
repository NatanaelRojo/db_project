# Generated by Django 4.1.1 on 2022-10-11 17:02

import accounts.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 11, 17, 2, 14, 158105, tzinfo=datetime.timezone.utc), verbose_name='creation date'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='00000000000', max_length=11, validators=[accounts.models.phone_number_validator]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]