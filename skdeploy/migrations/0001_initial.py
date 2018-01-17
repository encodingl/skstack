# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-19 02:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('skaccounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_english', models.CharField(max_length=50, verbose_name='\u82f1\u6587\u7b80\u79f0')),
                ('desc', models.CharField(blank=True, max_length=300, null=True, verbose_name='\u63cf\u8ff0')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u540d\u5b57')),
                ('desc', models.CharField(max_length=300, verbose_name='\u9879\u76ee\u63cf\u8ff0')),
                ('status', models.CharField(choices=[(b'no', '\u505c\u7528'), (b'yes', '\u6fc0\u6d3b')], default='no', max_length=10, verbose_name='\u9879\u76ee\u72b6\u6001')),
                ('repo_url', models.CharField(blank=True, max_length=100, null=True, verbose_name='git\u5730\u5740')),
                ('repo_mode', models.CharField(blank=True, choices=[(b'tag', 'tag'), (b'branch', 'branch'), (b'other', 'other')], max_length=50, null=True, verbose_name='\u4e0a\u7ebf\u65b9\u5f0f\uff1abranch/tag')),
                ('repo_type', models.CharField(blank=True, choices=[(b'git', 'git'), (b'other', 'other')], max_length=50, null=True, verbose_name='\u9879\u76ee\u7c7b\u578b\uff1agit/other')),
                ('release_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u76ee\u6807\u673a\u5668\u7528\u6237')),
                ('release_to', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u76ee\u6807\u673a\u5668\u7684\u76ee\u5f55\uff0c\u76f8\u5f53\u4e8enginx\u7684root\uff0c\u53ef\u76f4\u63a5web\u8bbf\u95ee')),
                ('release_library', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u76ee\u6807\u673a\u5668\u7248\u672c\u53d1\u5e03\u5e93')),
                ('hosts', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u76ee\u6807\u673a\u5668\u5217\u8868')),
                ('pre_deploy', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u90e8\u7f72\u524d\u7f6e\u4efb\u52a1pre-deploy')),
                ('post_deploy', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u540c\u6b65\u4e4b\u524d\u4efb\u52a1post-deploy')),
                ('pre_release', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u540c\u6b65\u4e4b\u540e\u66f4\u6539\u8f6f\u94fe\u63a5\u4e4b\u524d\u76ee\u6807\u673a\u5668\u6267\u884c\u7684\u4efb\u52a1pre-release')),
                ('post_release', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u76ee\u6807\u673a\u5668\u66f4\u6539\u8f6f\u8fde\u63a5\u540e\u6267\u884c\u7684\u4efb\u52a1post-release')),
                ('post_release_delay', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u76ee\u6807\u673a\u6267\u884cpost_release\u4efb\u52a1\u95f4\u9694/\u5ef6\u8fdf\u65f6\u95f4 \u5355\u4f4d:\u79d2')),
                ('audit_enable', models.BooleanField(verbose_name='\u662f\u5426\u5f00\u542f\u5ba1\u6838')),
                ('keep_version_num', models.PositiveIntegerField(blank=True, null=True, verbose_name='\u7ebf\u4e0a\u7248\u672c\u4fdd\u7559\u6570')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('template_enable', models.BooleanField(verbose_name='\u662f\u5426\u8f6c\u4e3a\u6a21\u677f')),
                ('audit_flow', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skaccounts.AuditFlow', verbose_name='\u5ba1\u6838\u6d41\u7a0b')),
                ('env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skdeploy.Environment', verbose_name='\u9879\u76ee\u73af\u5883')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u63cf\u8ff0')),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='\u4e0a\u7ebf\u6807\u9898')),
                ('desc', models.CharField(max_length=300, verbose_name='\u4e0a\u7ebf\u5185\u5bb9\u6982\u8ff0')),
                ('user_commit', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u7533\u8bf7\u4eba')),
                ('project', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('env', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u73af\u5883\u540d\u79f0')),
                ('project_group', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u9879\u76ee\u5206\u7ec4')),
                ('action', models.CharField(blank=True, choices=[(b'0', '\u4e0a\u7ebf'), (b'2', '\u56de\u6eda')], max_length=30, null=True, verbose_name='\u52a8\u4f5c')),
                ('status', models.CharField(blank=True, choices=[(b'0', '\u65b0\u5efa\u63d0\u4ea4'), (b'1', 'l1\u5ba1\u6838\u901a\u8fc7'), (b'2', 'l1\u5ba1\u6838\u62d2\u7edd'), (b'3', '\u4e0a\u7ebf\u6210\u529f'), (b'4', '\u4e0a\u7ebf\u5931\u8d25'), (b'5', 'l2\u5ba1\u6838\u901a\u8fc7'), (b'6', 'l2\u5ba1\u6838\u62d2\u7edd'), (b'7', 'l3\u5ba1\u6838\u901a\u8fc7'), (b'8', 'l3\u5ba1\u6838\u62d2\u7edd'), (b'9', '\u64a4\u9500')], max_length=30, null=True, verbose_name='\u72b6\u6001')),
                ('link_id', models.CharField(max_length=50, verbose_name='\u5f53\u524d\u4e0a\u7ebf\u7684\u8f6f\u94fe\u53f7')),
                ('ex_link_id', models.CharField(max_length=50, verbose_name='\u4e0a\u4e00\u6b21\u4e0a\u7ebf\u7684\u8f6f\u94fe\u53f7')),
                ('commit_id', models.CharField(max_length=50, verbose_name='git commit id')),
                ('branch', models.CharField(max_length=50, verbose_name='\u4e0a\u7ebf\u7684\u5206\u652f')),
                ('enable_rollback', models.CharField(max_length=50, verbose_name='\u80fd\u5426\u56de\u6eda\u6b64\u7248\u672c:')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u63d0\u5355\u65f6\u95f4')),
                ('audit_level', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5ba1\u6838\u5c42\u7ea7')),
                ('user_l1', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u7b2c1\u7ea7\u5ba1\u6838\u7528\u6237')),
                ('updated_at_l1', models.DateTimeField(null=True, verbose_name='l1\u5ba1\u6838\u65f6\u95f4')),
                ('user_l2', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u7b2c2\u7ea7\u5ba1\u6838\u7528\u6237')),
                ('updated_at_l2', models.DateTimeField(null=True, verbose_name='l2\u5ba1\u6838\u65f6\u95f4')),
                ('user_l3', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u7b2c3\u7ea7\u5ba1\u6838\u7528\u6237')),
                ('updated_at_l3', models.DateTimeField(null=True, verbose_name='l3\u5ba1\u6838\u65f6\u95f4')),
                ('finished_at', models.DateTimeField(null=True, verbose_name='\u5b8c\u6210\u65f6\u95f4')),
                ('project_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u9879\u76eeid')),
                ('forks', models.PositiveIntegerField(blank=True, null=True, verbose_name='\u5e76\u53d1\u7cfb\u6570\uff0c\u8bf7\u8f93\u5165\u4e00\u4e2a\u6b63\u6574\u6570\uff0c\u9ed8\u8ba4\u503c\u4e3a\u9879\u76ee\u5b9e\u4f8b\u7684\u4e00\u534a')),
                ('hosts_cus', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u81ea\u5b9a\u4e49\u76ee\u6807\u4e3b\u673a(\u8fd0\u7ef4\u4f7f\u7528)')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skdeploy.ProjectGroup', verbose_name='\u9879\u76ee\u5206\u7ec4'),
        ),
        migrations.AddField(
            model_name='project',
            name='user_dep',
            field=models.ManyToManyField(blank=True, to='skaccounts.UserGroup', verbose_name='\u63d0\u5355\u6743\u9650\u7528\u6237'),
        ),
    ]