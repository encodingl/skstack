#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from skaccounts.models import UserGroup

# Create your models here.

import datetime
from _mysql import NULL
from celery.bin.control import status

TASK_STATUS = (
    (str(0), u"新建提交"),
    (str(1), u"l1审核通过"),
    (str(2), u"l1审核拒绝"),
    (str(3), u"上线完成"),
    (str(4), u"上线失败"),
    (str(5), u"l2审核通过"),
    (str(6), u"l2审核拒绝"),
    (str(7), u"l3审核通过"),
    (str(8), u"l3审核拒绝"),
    )

PROJECT_STATUS = (
    (str(0), u"停用"),
    (str(1), u"激活"),
    )

PROJECT_SOURCE = (
    (str(0), u"skipper"),
    (str(1), u"walle"),
    )

TASK_ACTION = (
    (str(0), u"上线"),
    (str(2), u"回滚"),
    )
# Create your models here.
class AuditFlow(models.Model):
    name = models.CharField(u"登录用户",max_length=50)
    level = models.IntegerField(u"审核层级",max_length=50)
    user_l1 = models.ForeignKey(UserGroup, verbose_name=u"第1级审核用户组", on_delete=models.SET_NULL, null=True, blank=True)
    user_l2 = models.ForeignKey(UserGroup, verbose_name=u"第2级审核用户组", on_delete=models.SET_NULL, null=True, blank=True)
    user_l3 = models.ForeignKey(UserGroup, verbose_name=u"第3级审核用户组", on_delete=models.SET_NULL, null=True, blank=True)
    def __unicode__(self):
        return self.name
    
    
class Environment(models.Model):
    name  = models.CharField(u"环境名称",max_length=50)
    name_english  = models.CharField(u"英文简称",max_length=50)
    desc = models.CharField(u"描述", max_length=300, null=True, blank=True)
    
    def __unicode__(self):
        return self.name

    
class Project(models.Model):   
    name = models.CharField(u"项目名字",max_length=50)
    name_english  = models.CharField(u"英文简称",max_length=50)
    source = models.CharField(u"项目来源", choices=PROJECT_SOURCE, max_length=30, null=True, blank=True)
    user_create_proj = models.CharField(u"添加项目的用户",max_length=50)
    user_dep = models.ManyToManyField(UserGroup, verbose_name=u"具有发布申请权限的用户", on_delete=models.SET_NULL, null=True, blank=True)
    evn = models.ForeignKey(Environment, verbose_name=u"项目环境", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(u"激活状态", choices=PROJECT_STATUS, max_length=30, null=True, blank=True)
    repo_url = models.CharField(u"git地址",max_length=100,null=True, blank=True)
    repo_mode = models.CharField(u"上线方式：branch/tag",max_length=50,null=True, blank=True)
    repo_type = models.CharField(u"上线方式：git/other",max_length=50,null=True, blank=True)  
    release_user = models.CharField(u"目标机器用户",max_length=50,null=True, blank=True)
    release_to = models.CharField(u"目标机器的目录，相当于nginx的root，可直接web访问",max_length=50,null=True, blank=True)
    release_library = models.CharField(u"目标机器版本发布库",max_length=50,null=True, blank=True)
    hosts = models.CharField(u"目标机器列表",max_length=50,null=True, blank=True)
    pre_deploy = models.CharField(u"部署前置任务",max_length=200,null=True, blank=True)
    post_deploy = models.CharField(u"同步之前任务",max_length=200,null=True, blank=True)
    pre_release = models.CharField(u"同步之前目标机器执行的任务",max_length=200,null=True, blank=True)
    post_release = models.CharField(u"同步之后目标机器执行的任务",max_length=200,null=True, blank=True)
    post_release_delay = models.CharField(u"每台目标机执行post_release任务间隔/延迟时间 单位:秒",max_length=50,null=True, blank=True)
    audit_enable = models.CharField(u"是否需要审核任务0不需要，1需要",max_length=50,null=True, blank=True)
    audit_flow = models.ForeignKey(AuditFlow, verbose_name=u"审核流程", on_delete=models.SET_NULL, null=True, blank=True)
    keep_version_num = models.CharField(u"线上版本保留数",max_length=50,null=True, blank=True)
    created_at = models.DateTimeField(u'创建时间', auto_now_add=True,null=True)
    updated_at = models.DateTimeField(u'修改时间', auto_now_add=True,null=True)
    def __unicode__(self):
        return self.name
    
class Task(models.Model):
    user_id = models.CharField(u"登录用户",max_length=50)
    project_id = models.ForeignKey(Project, verbose_name=u"所属项目", on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(u"动作", choices=TASK_ACTION, max_length=30, null=True, blank=True)
    status = models.CharField(u"激活状态", choices=TASK_STATUS, max_length=30, null=True, blank=True)
    title = models.CharField(u"登录用户",max_length=50)
    link_id = models.CharField(u"上线的软链号",max_length=50)
    ex_link_id = models.CharField(u"上一次上线的软链号",max_length=50)
    commit_id = models.CharField(u"git commit id",max_length=50)
    branch = models.CharField(u"上线的分支",max_length=50)
    enable_rollback = models.CharField(u"能否回滚此版本:0no 1yes",max_length=50)
    created_at = models.DateTimeField(u'创建时间', auto_now_add=True,null=True)
    updated_at_l1 = models.DateTimeField(u'l1审核时间', auto_now_add=True,null=True)
    updated_at_l2 = models.DateTimeField(u'l2审核时间', auto_now_add=True,null=True)
    updated_at_l3 = models.DateTimeField(u'l3审核时间', auto_now_add=True,null=True)
    def __unicode__(self):
        return self.project_id
    
