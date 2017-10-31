# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-23 09:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skyw', '0005_auto_20171023_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rota',
            name='rota_name',
        ),
        migrations.AddField(
            model_name='rota',
            name='rota_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rota_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
