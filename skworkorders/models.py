#! /usr/bin/env python
# -*- coding: utf-8 -*-

#x6

from __future__ import unicode_literals

from django.db import models
from skaccounts.models import UserGroup,AuditFlow


# Create your models here.3

import datetime
from _mysql import NULL
from celery.bin.control import status



WorkOrder_STATUS = (
    (str("no"), u"停用"),
    (str("yes"), u"激活"),
    )

WorkOrder_SOURCE = (
    (str("skipper"), u"skipper"),
    (str("local"), u"local"),
    )

WorkOrder_REPO_MODE = (
    (str("tag"), u"tag"),
    (str("branch"), u"branch"),
    (str("other"), u"other"),
    )
WorkOrder_REPO_TYPE = (
    (str("git"), u"git"),
    (str("other"), u"other"),
    )

TASK_ACTION = (
    (str(0), u"上线"),
    (str(2), u"回滚"),
    )

TASK_STATUS = (
    (str(0), u"新建提交"),
    (str(1), u"l1审核通过"),
    (str(2), u"l1审核拒绝"),
    (str(3), u"上线成功"),
    (str(4), u"上线失败"),
    (str(5), u"l2审核通过"),
    (str(6), u"l2审核拒绝"),
    (str(7), u"l3审核通过"),
    (str(8), u"l3审核拒绝"),
    (str(9), u"撤销"),
    )



WorkOrder_AUDIT_ENABLE = (
    (str("no"), u"关闭"),
    (str("yes"), u"开启"),
    )
# Create your models here.

    
    
class Environment(models.Model):
    
    name_english  = models.CharField(u"英文简称",max_length=50)
    desc = models.CharField(u"描述", max_length=300, null=True, blank=True)
    
    def __unicode__(self):
        return self.name_english
    
class WorkOrdersGroup(models.Model):
    name = models.CharField(max_length=100)    # permission = models.ManyToManyField(PermissionList, null=True, blank=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name
class Dynamic_vars(models.Model): 
    name = models.CharField(u"项目名字",max_length=50)
    desc  = models.CharField(u"项目描述",max_length=300)
    script = models.CharField(u"获取变量的脚本",max_length=200,null=True, blank=True)
    
    
class WorkOrders(models.Model):   
    name = models.CharField(u"项目名字",max_length=50)
    desc  = models.CharField(u"项目描述",max_length=300)  
    user_dep = models.ManyToManyField(UserGroup, verbose_name=u"提单权限用户",blank=True)
    env = models.ForeignKey(Environment, verbose_name=u"项目环境", on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(WorkOrdersGroup, verbose_name=u"项目分组", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(u"项目状态", choices=WorkOrder_STATUS, max_length=10,default="no")
    
    hosts = models.CharField(u"目标机器列表",max_length=50,null=True, blank=True)
    cus_var_switch = models.CharField(u"自定义变量开关",max_length=200,null=True, blank=True)
    cus_var1 = models.ForeignKey(Dynamic_vars, verbose_name=u"动态变量1", on_delete=models.SET_NULL, null=True, blank=True)
    cus_var2 = models.ForeignKey(Dynamic_vars, verbose_name=u"动态变量2", on_delete=models.SET_NULL, null=True, blank=True)
  
    
    pre_task = models.CharField(u"前置任务",max_length=200,null=True, blank=True)
    main_task = models.CharField(u"主任务",max_length=200,null=True, blank=True)
    post_task = models.CharField(u"后置任务",max_length=200,null=True, blank=True)
   
    audit_enable = models.BooleanField(u"是否开启审核")
    audit_flow = models.ForeignKey(AuditFlow, verbose_name=u"审核流程", on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(u'创建时间', auto_now_add=True,null=True)
    updated_at = models.DateTimeField(u'修改时间', auto_now_add=True,null=True)
    template_enable = models.BooleanField(u"是否转为模板")
    
    def __unicode__(self):
        return self.name
    
class TaskStatus(models.Model):
    title = models.CharField(u"标题",max_length=50)
    desc  = models.CharField(u"内容概述",max_length=300)
    user_commit = models.CharField(u"申请人",max_length=50,null=True,blank=True)
    project = models.CharField(u"项目名称",max_length=50,null=True,blank=True)
    env = models.CharField(u"环境名称",max_length=50,null=True,blank=True)
    WorkOrder_group = models.CharField(u"项目分组",max_length=50,null=True,blank=True)
    action = models.CharField(u"动作", choices=TASK_ACTION, max_length=30, null=True, blank=True)
    status = models.CharField(u"状态", choices=TASK_STATUS, max_length=30, null=True, blank=True)  
    link_id = models.CharField(u"当前上线的软链号",max_length=50)
    ex_link_id = models.CharField(u"上一次上线的软链号",max_length=50)
    commit_id = models.CharField(u"git commit id",max_length=50)
    branch = models.CharField(u"上线的分支",max_length=50)
    enable_rollback = models.CharField(u"能否回滚此版本:",max_length=50)
    created_at = models.DateTimeField(u'提单时间', auto_now_add=True,null=True)
    audit_level = models.CharField(u"审核层级",max_length=50,null=True,blank=True)
    user_l1 = models.CharField(u"第1级审核用户",max_length=50,null=True,blank=True)
    updated_at_l1 = models.DateTimeField(u'l1审核时间', null=True)
    user_l2 = models.CharField(u"第2级审核用户",max_length=50,null=True,blank=True)
    updated_at_l2 = models.DateTimeField(u'l2审核时间', null=True)
    user_l3 = models.CharField(u"第3级审核用户",max_length=50,null=True,blank=True)
    updated_at_l3 = models.DateTimeField(u'l3审核时间', null=True)
    finished_at = models.DateTimeField(u'完成时间',null=True)
    WorkOrder_id = models.CharField(u"项目id",max_length=50,null=True,blank=True)
    forks = models.PositiveIntegerField(u"并发系数，请输入一个正整数，默认值为项目实例的一半", null=True, blank=True)
    hosts_cus = models.CharField(u"自定义目标主机(运维使用)",max_length=200,null=True,blank=True)
    def __unicode__(self):
        return self.title
    
