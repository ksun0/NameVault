# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 14:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 12, 10, 41, 55, 810495), verbose_name='date joined'),
        ),
    ]
