#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from skcmdb.models import YwGroup
from skaccounts.models import UserInfo,UserGroup


class PlatFormclass(models.Model):
    platform_class = models.CharField("平台分类", max_length=15,null=True, blank=True)
    def __str__(self):
      return self.platform_class

class Platform(models.Model):
    platform_class = models.ManyToManyField(PlatFormclass,blank=True)
    platform_name = models.CharField("平台名称",max_length=15)
    platform_url = models.URLField("平台url",max_length=60)
    def __str__(self):
      return self.platform_name

class event(models.Model):
    level = models.CharField("等级",max_length=15)
    responsetime = models.CharField("响应时间",max_length=15)
    processingpersonnel = models.CharField("跟进人员",max_length=15)
    event = models.CharField("处理问题和升级流程",max_length=200)
    participant = models.CharField("参与人员",max_length=200)
    def __str__(self):
      return self.platform_level

class Devops(models.Model):
    JOB = (
        (0,'应用运维'),
        (1,'系统运维'),
        (2,'基础运维'),
        (3,'dba运维'),
        (4,'IT支持'),
    )
    name = models.ForeignKey(UserInfo,related_name='nicknames',on_delete=models.SET_NULL, null=True, blank=True)
    #job  = models.ForeignKey(UserInfo,related_name='types',on_delete=models.SET_NULL, null=True, blank=True)
    job = models.IntegerField(choices=JOB,verbose_name='运维角色',null=True)
    iphone = models.CharField('联系方式',max_length=20)
    jobclass = models.CharField('运维系统分工',max_length=100)
    businessline = models.ManyToManyField(YwGroup)
    secondaryname = models.ForeignKey(UserInfo,related_name='nickname_backup',on_delete=models.SET_NULL, null=True, blank=True)
    jobuse = models.CharField('运维工具',max_length=15)

    def __str__(self):
      return self.iphone


class Rota(models.Model):
    SPELL_TYPE=((0,'是'),(1,'否'))
    EMERGENCY_type=((0,'是'),(1,'否'))
    IPHONE_ROTA=((0,'是'),(1,'否'))
    name = models.ForeignKey(UserInfo,related_name='rota_name',null=True, blank=False,on_delete=models.SET_NULL)
    iphone = models.ForeignKey(Devops,related_name='rota_iphone',on_delete=models.SET_NULL, null=True, blank=False)
    spell = models.IntegerField(choices=SPELL_TYPE,verbose_name='是否轮值',null=False)
    emergency_contact = models.IntegerField(choices=SPELL_TYPE,verbose_name='是否为重要联系人',null=False)
    iphone_rota = models.IntegerField(choices=IPHONE_ROTA,verbose_name='是否电话值班',null=False)
    rota_number=models.CharField('值班顺序',max_length=15,null=True, blank=False)
    # iphone_rota = models.IntegerField(choices=IPHONE_ROTA,verbose_name='是否电话值班',null=False, blank=False)

    def __str__(self):
        return self.name

class Notice(models.Model):
    notice= models.TextField('公告内容',max_length=200)
    def __str__(self):
        return self.notice
