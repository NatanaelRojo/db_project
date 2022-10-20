# Generated by Django 4.1.1 on 2022-10-12 20:53

import accounts.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_creation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='identification',
            field=models.CharField(default='V000000000', max_length=10, validators=[accounts.models.identification_validator]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 12, 20, 53, 25, 826419, tzinfo=datetime.timezone.utc), verbose_name='creation date'),
        ),
    ]
