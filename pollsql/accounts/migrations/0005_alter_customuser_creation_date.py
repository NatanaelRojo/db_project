# Generated by Django 4.1.1 on 2022-10-17 22:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_identification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 17, 22, 51, 20, 270225, tzinfo=datetime.timezone.utc), verbose_name='creation date'),
        ),
    ]