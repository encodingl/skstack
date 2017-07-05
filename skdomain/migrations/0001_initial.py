# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-05 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='navi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('description', models.CharField(max_length=50, verbose_name='\u63cf\u8ff0')),
                ('url', models.URLField(verbose_name='\u7f51\u5740')),
                ('online_status', models.CharField(blank=True, choices=[(b'0', '\u672a\u542f\u7528'), (b'1', '\u542f\u7528'), (b'2', '\u5df2\u4e0b\u7ebf')], max_length=30, null=True, verbose_name='online_status')),
            ],
        ),
        migrations.CreateModel(
            name='WhiteList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
                ('description', models.CharField(max_length=50, verbose_name='\u63cf\u8ff0')),
            ],
        ),
        migrations.AddField(
            model_name='navi',
            name='white_list',
            field=models.ManyToManyField(blank=True, to='skdomain.WhiteList', verbose_name='\u767d\u540d\u5355'),
        ),
    ]
