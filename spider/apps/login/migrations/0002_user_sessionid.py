# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-04 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sessionid',
            field=models.CharField(default='null', max_length=40),
        ),
    ]
