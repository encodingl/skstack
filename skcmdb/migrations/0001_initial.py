# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-19 02:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='* APP\u540d\u79f0')),
                ('web_port', models.IntegerField(blank=True, null=True, verbose_name='Web\u7aef\u53e3\u53f7')),
                ('dubbo_port', models.IntegerField(blank=True, null=True, verbose_name='Dubbo\u7aef\u53e3\u53f7')),
                ('status', models.CharField(blank=True, choices=[(b'1', '\u4f7f\u7528\u4e2d'), (b'2', '\u672a\u4f7f\u7528'), (b'3', '\u6545\u969c'), (b'4', '\u5176\u5b83')], max_length=30, null=True, verbose_name='\u8bbe\u5907\u72b6\u6001')),
                ('descrition', models.TextField(blank=True, max_length=200, null=True, verbose_name='\u5907\u6ce8\u4fe1\u606f')),
            ],
        ),
        migrations.CreateModel(
            name='DbSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='* \u540d\u79f0')),
                ('host', models.GenericIPAddressField(null=True, verbose_name='\u4e3b\u673aip')),
                ('user', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u7528\u6237\u540d')),
                ('password', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5bc6\u7801')),
                ('port', models.IntegerField(blank=True, default=3306, null=True, verbose_name='\u7aef\u53e3\u53f7')),
                ('db', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u6570\u636e\u5e93\u540d')),
            ],
        ),
        migrations.CreateModel(
            name='Env',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='* \u73af\u5883\u540d\u79f0')),
                ('descrition', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u63cf\u8ff0')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=50, unique=True, verbose_name='* \u4e3b\u673a\u540d')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='* IP\u5730\u5740')),
                ('other_ip', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u5176\u5b83IP')),
                ('asset_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u8d44\u4ea7\u7f16\u53f7')),
                ('status', models.CharField(blank=True, choices=[(b'1', '\u4f7f\u7528\u4e2d'), (b'2', '\u672a\u4f7f\u7528'), (b'3', '\u6545\u969c'), (b'4', '\u5176\u5b83')], max_length=30, null=True, verbose_name='\u8bbe\u5907\u72b6\u6001')),
                ('os', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf')),
                ('vendor', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u8bbe\u5907\u5382\u5546')),
                ('cpu_model', models.CharField(blank=True, max_length=100, null=True, verbose_name='CPU\u578b\u53f7')),
                ('cpu_num', models.CharField(blank=True, max_length=100, null=True, verbose_name='CPU\u6570\u91cf')),
                ('memory', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5185\u5b58\u5927\u5c0f')),
                ('disk', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u786c\u76d8\u4fe1\u606f')),
                ('sn', models.CharField(blank=True, max_length=60, verbose_name='SN\u53f7 \u7801')),
                ('position', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u6240\u5728\u4f4d\u7f6e')),
                ('memo', models.TextField(blank=True, max_length=200, null=True, verbose_name='\u5907\u6ce8\u4fe1\u606f')),
                ('env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.Env', verbose_name='\u8fd0\u884c\u73af\u5883')),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='* \u7ec4\u540d')),
                ('desc', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u63cf\u8ff0')),
            ],
        ),
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True, verbose_name='* \u673a\u623f\u540d\u79f0')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u673a\u623f\u5730\u5740')),
                ('tel', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u673a\u623f\u7535\u8bdd')),
                ('contact', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5ba2\u6237\u7ecf\u7406')),
                ('contact_phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u79fb\u52a8\u7535\u8bdd')),
                ('jigui', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u673a\u67dc\u4fe1\u606f')),
                ('ip_range', models.CharField(blank=True, max_length=30, null=True, verbose_name='IP\u8303\u56f4')),
                ('bandwidth', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u63a5\u5165\u5e26\u5bbd')),
            ],
            options={
                'verbose_name': '\u6570\u636e\u4e2d\u5fc3',
                'verbose_name_plural': '\u6570\u636e\u4e2d\u5fc3',
            },
        ),
        migrations.CreateModel(
            name='InterFace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('vendor', models.CharField(max_length=30, null=True)),
                ('bandwidth', models.CharField(max_length=30, null=True)),
                ('tel', models.CharField(max_length=30, null=True)),
                ('contact', models.CharField(max_length=30, null=True)),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('price', models.IntegerField(verbose_name='\u4ef7\u683c')),
            ],
        ),
        migrations.CreateModel(
            name='IpSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('net', models.CharField(max_length=30)),
                ('subnet', models.CharField(max_length=30, null=True)),
                ('describe', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KafkaTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='* App\u540d\u79f0')),
                ('descrition', models.TextField(blank=True, max_length=200, null=True, verbose_name='\u5907\u6ce8\u4fe1\u606f')),
            ],
        ),
        migrations.CreateModel(
            name='MiddleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='* \u4e3b\u673a\u7ec4\u540d\u79f0')),
                ('descrition', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u63cf\u8ff0')),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='* Url\u540d\u79f0')),
                ('nickname', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u4e1a\u52a1\u540d\u79f0')),
                ('mapip', models.GenericIPAddressField(blank=True, null=True, verbose_name='\u6620\u5c04IP')),
                ('type', models.CharField(blank=True, choices=[(b'1', '\u5916\u7f51'), (b'2', '\u5185\u7f51')], max_length=30, null=True, verbose_name='\u7c7b\u578b')),
                ('status', models.CharField(blank=True, choices=[(b'1', '\u4f7f\u7528\u4e2d'), (b'2', '\u672a\u4f7f\u7528'), (b'3', '\u6545\u969c'), (b'4', '\u5176\u5b83')], max_length=30, null=True, verbose_name='\u8bbe\u5907\u72b6\u6001')),
                ('descrition', models.TextField(blank=True, max_length=1000, null=True, verbose_name='\u7528\u9014')),
                ('belongapp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.App', verbose_name='\u6240\u5c5eApp')),
                ('env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.Env', verbose_name='\u8fd0\u884c\u73af\u5883')),
                ('sa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='\u8fd0\u7ef4\u8d1f\u8d23\u4eba')),
            ],
        ),
        migrations.CreateModel(
            name='WhileIp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=50, unique=True, verbose_name='* \u767d\u540d\u5355')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u540d\u79f0')),
                ('descrition', models.TextField(blank=True, max_length=1000, null=True, verbose_name='\u7528\u9014')),
            ],
        ),
        migrations.CreateModel(
            name='YwGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='* \u5c0f\u7ec4\u540d\u79f0')),
                ('sa', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u8d1f\u8d23\u4eba')),
                ('descrition', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u63cf\u8ff0')),
            ],
        ),
        migrations.AddField(
            model_name='url',
            name='whitelist',
            field=models.ManyToManyField(blank=True, to='skcmdb.WhileIp', verbose_name='\u767d\u540d\u5355\u5217\u8868'),
        ),
        migrations.AddField(
            model_name='url',
            name='ywgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.YwGroup', verbose_name='\u4e1a\u52a1\u5206\u7ec4'),
        ),
        migrations.AddField(
            model_name='host',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.HostGroup', verbose_name='\u4e3b\u673a\u5206\u7ec4'),
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.Idc', verbose_name='\u6240\u5728\u673a\u623f'),
        ),
        migrations.AddField(
            model_name='host',
            name='middletype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.MiddleType', verbose_name='\u4e3b\u673a\u7c7b\u578b'),
        ),
        migrations.AddField(
            model_name='host',
            name='sa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='\u8d1f\u8d23\u4eba'),
        ),
        migrations.AddField(
            model_name='host',
            name='ywgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.YwGroup', verbose_name='\u4e1a\u52a1\u5206\u7ec4'),
        ),
        migrations.AddField(
            model_name='env',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.Idc', verbose_name='\u6240\u5728\u673a\u623f'),
        ),
        migrations.AddField(
            model_name='app',
            name='belong_ip',
            field=models.ManyToManyField(blank=True, to='skcmdb.Host', verbose_name='\u6240\u5c5e\u4e3b\u673a'),
        ),
        migrations.AddField(
            model_name='app',
            name='env',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.Env', verbose_name='\u8fd0\u884c\u73af\u5883'),
        ),
        migrations.AddField(
            model_name='app',
            name='kafka',
            field=models.ManyToManyField(blank=True, to='skcmdb.KafkaTopic', verbose_name='Kafka\u5217\u8868'),
        ),
        migrations.AddField(
            model_name='app',
            name='sa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='\u8fd0\u7ef4\u8d1f\u8d23\u4eba'),
        ),
        migrations.AddField(
            model_name='app',
            name='ywgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skcmdb.YwGroup', verbose_name='\u4e1a\u52a1\u5206\u7ec4'),
        ),
    ]