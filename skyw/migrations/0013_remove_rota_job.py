# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-25 08:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skyw', '0012_rota_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rota',
            name='job',
        ),
    ]
