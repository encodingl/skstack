#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from _mysql import NULL

ONLINE_STATUS = (
    (str(0), u"停用"),
    (str(1), u"激活"),
    )
# Create your models here.
class history(models.Model):
    login_user = models.CharField(u"登录用户",max_length=50)
    src_ip = models.CharField(u"来源ip",max_length=50)    
    task_name = models.CharField(u"任务类型",max_length=50,default="none")
    time_task_start=models.DateTimeField(u'开始时间',null=True)
    time_task_finished=models.DateTimeField(u'结束时间', auto_now_add=True,null=True)
    cmd_object = models.CharField(u"操作对象",max_length=50,null=True)
    cmd = models.CharField(u"执行命令",max_length=200)
    cmd_result = models.CharField(u"命令结果",max_length=10)
    cmd_detail = models.CharField(u"结果详情",max_length=5000,null=True, blank=True)
        
    def __unicode__(self):
        return self.cmd_result
    class Meta:
        ordering=['-id']


class project(models.Model):
    name = models.CharField(u"项目名",max_length=50)
    path = models.CharField(u"项目路径",max_length=50)
    online_status = models.CharField(u"激活状态", choices=ONLINE_STATUS, max_length=30, null=True, blank=True)  
    def __unicode__(self):
        return self.name
    

class job(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"作业名", unique=True)
    playbook = models.CharField(u"playbook", max_length=100, null=True, blank=True)
    project = models.ForeignKey(project, verbose_name=u"所属项目", on_delete=models.SET_NULL, null=True, blank=True)
    online_status = models.CharField(u"激活状态", choices=ONLINE_STATUS, max_length=30, null=True, blank=True)
    def __unicode__(self):
        return self.name
    
class extravars(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"变量组名", unique=True)
    vars= models.CharField(u"配置参数", max_length=150, null=True, blank=True)
    job = models.ForeignKey(job, verbose_name=u"所属作业", on_delete=models.SET_NULL, null=True, blank=True)
    online_status = models.CharField(u"激活状态", choices=ONLINE_STATUS, max_length=30, null=True, blank=True)
    def __unicode__(self):
        return self.name
    
    