# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-21 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examRetake_python', '0004_auto_20180821_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userThatCreatedThisTrip', to='examRetake_python.User'),
        ),
    ]
