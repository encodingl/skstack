#! /usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
import datetime
# from _mysql import NULL


ONLINE_STATUS = (
    (str(0), "停用"),
    (str(1), "激活"),
    )
# Create your models here.
class history(models.Model):
    login_user = models.CharField("登录用户",max_length=50)
    src_ip = models.CharField("来源ip",max_length=50)    
    task_name = models.CharField("任务类型",max_length=50,default="none")
    time_task_start=models.DateTimeField('开始时间',null=True)
    time_task_finished=models.DateTimeField('结束时间', auto_now_add=True,null=True)
    cmd_object = models.CharField("操作对象",max_length=50,null=True)
    cmd = models.CharField("执行命令",max_length=200)
    cmd_result = models.CharField("命令结果",max_length=10)
    cmd_detail = models.CharField("结果详情",max_length=5000,null=True, blank=True)
        
    def __str__(self):
        return self.cmd_result
    class Meta:
        ordering=['-id']


class project(models.Model):
    name = models.CharField("项目名",max_length=50)
    path = models.CharField("项目路径",max_length=50)
    online_status = models.CharField("激活状态", choices=ONLINE_STATUS, max_length=30, null=True, blank=True)  
    def __str__(self):
        return self.name
    

class job(models.Model):
    name = models.CharField(max_length=50, verbose_name="作业名", unique=True)
    playbook = models.CharField("playbook", max_length=100, null=True, blank=True)
    project = models.ForeignKey(project, verbose_name="所属项目", on_delete=models.SET_NULL, null=True, blank=True)
    online_status = models.CharField("激活状态", choices=ONLINE_STATUS, max_length=30, null=True, blank=True)
    def __str__(self):
        return self.name
    
class extravars(models.Model):
    name = models.CharField(max_length=50, verbose_name="变量组名", unique=True)
    vars= models.CharField("配置参数", max_length=150, null=True, blank=True)
    job = models.ForeignKey(job, verbose_name="所属作业", on_delete=models.SET_NULL, null=True, blank=True)
    online_status = models.CharField("激活状态", choices=ONLINE_STATUS, max_length=30, null=True, blank=True)
    def __str__(self):
        return self.name
    
    