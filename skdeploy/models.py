#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from skaccounts.models import UserGroup,AuditFlow


# Create your models here.3

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
    (str("no"), u"停用"),
    (str("yes"), u"激活"),
    )

PROJECT_SOURCE = (
    (str("skipper"), u"skipper"),
    (str("local"), u"local"),
    )

PROJECT_REPO_MODE = (
    (str("tag"), u"tag"),
    (str("branch"), u"branch"),
    (str("other"), u"other"),
    )
PROJECT_REPO_TYPE = (
    (str("git"), u"git"),
    (str("other"), u"other"),
    )

TASK_ACTION = (
    (str(0), u"上线"),
    (str(2), u"回滚"),
    )

PROJECT_AUDIT_ENABLE = (
    (str("no"), u"关闭"),
    (str("yes"), u"开启"),
    )
# Create your models here.

    
    
class Environment(models.Model):
    
    name_english  = models.CharField(u"英文简称",max_length=50)
    desc = models.CharField(u"描述", max_length=300, null=True, blank=True)
    
    def __unicode__(self):
        return self.name_english
    
class ProjectGroup(models.Model):
    name = models.CharField(max_length=100)    # permission = models.ManyToManyField(PermissionList, null=True, blank=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

    
class Project(models.Model):   
    name = models.CharField(u"项目名字",max_length=50)
    desc  = models.CharField(u"项目描述",max_length=300, null=True, blank=True)  
    user_dep = models.ManyToManyField(UserGroup, verbose_name=u"提单权限用户", null=True, blank=True)
    env = models.ForeignKey(Environment, verbose_name=u"项目环境", on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(ProjectGroup, verbose_name=u"项目分组", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(u"项目状态", choices=PROJECT_STATUS, max_length=30, null=True, blank=True)
    repo_url = models.CharField(u"git地址",max_length=100,null=True, blank=True)
    repo_mode = models.CharField(u"上线方式：branch/tag",choices=PROJECT_REPO_MODE,max_length=50,null=True, blank=True)
    repo_type = models.CharField(u"上线方式：git/other",choices=PROJECT_REPO_TYPE,max_length=50,null=True, blank=True)  
    release_user = models.CharField(u"目标机器用户",max_length=50,null=True, blank=True)
    release_to = models.CharField(u"目标机器的目录，相当于nginx的root，可直接web访问",max_length=50,null=True, blank=True)
    release_library = models.CharField(u"目标机器版本发布库",max_length=50,null=True, blank=True)
    hosts = models.CharField(u"目标机器列表",max_length=50,null=True, blank=True)
    pre_deploy = models.CharField(u"部署前置任务pre-deploy",max_length=200,null=True, blank=True)
    post_deploy = models.CharField(u"同步之前任务post-deploy",max_length=200,null=True, blank=True)
    pre_release = models.CharField(u"同步之后更改软链接之前目标机器执行的任务pre-release",max_length=200,null=True, blank=True)
    post_release = models.CharField(u"目标机器更改软连接后执行的任务post-release",max_length=200,null=True, blank=True)
    post_release_delay = models.CharField(u"每台目标机执行post_release任务间隔/延迟时间 单位:秒",max_length=50,null=True, blank=True)
    audit_enable = models.CharField(u"是否开启审核",choices=PROJECT_AUDIT_ENABLE,max_length=50,null=True, blank=True)
    audit_flow = models.ForeignKey(AuditFlow, verbose_name=u"审核流程", on_delete=models.SET_NULL, null=True, blank=True)
    keep_version_num = models.CharField(u"线上版本保留数",max_length=50,null=True, blank=True)
    created_at = models.DateTimeField(u'创建时间', auto_now_add=True,null=True)
    updated_at = models.DateTimeField(u'修改时间', auto_now_add=True,null=True)
    def __unicode__(self):
        return self.name
    
class TaskStatus(models.Model):
    title = models.CharField(u"上线标题",max_length=50)
    desc  = models.CharField(u"上线内容概述",max_length=300, null=True, blank=True)
    user_commit = models.CharField(u"申请人",max_length=50,null=True,blank=True)
    project = models.CharField(u"项目名称",max_length=50,null=True,blank=True)
    env = models.CharField(u"环境名称",max_length=50,null=True,blank=True)
    project_group = models.CharField(u"项目分组",max_length=50,null=True,blank=True)
    action = models.CharField(u"动作", choices=TASK_ACTION, max_length=30, null=True, blank=True)
    status = models.CharField(u"激活状态", choices=TASK_STATUS, max_length=30, null=True, blank=True)  
    link_id = models.CharField(u"本次上线的软链号",max_length=50)
    ex_link_id = models.CharField(u"上一次上线的软链号",max_length=50)
    commit_id = models.CharField(u"git commit id",max_length=50)
    branch = models.CharField(u"上线的分支",max_length=50)
    enable_rollback = models.CharField(u"能否回滚此版本:0no 1yes",max_length=50)
    created_at = models.DateTimeField(u'提单时间', auto_now_add=True,null=True)
    updated_at_l1 = models.DateTimeField(u'l1审核时间', null=True)
    updated_at_l2 = models.DateTimeField(u'l2审核时间', null=True)
    updated_at_l3 = models.DateTimeField(u'l3审核时间', null=True)
    finished_at = models.DateTimeField(u'完成时间',null=True)
    project_id = models.CharField(u"项目id",max_length=50,null=True,blank=True)
    def __unicode__(self):
        return self.title
    
