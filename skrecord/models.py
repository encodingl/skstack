#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


#EVENT_STATUS = (
#    (str(1), u"P0:服务完全不可用"),
#    (str(2), u"P1:个别业务的服务部分不可用"),
#    (str(3), u"P2:造成个别用户无法访问"),
#    (str(4), u"P3:无影响"),
#    )


class Record_list(models.Model):
    name = models.CharField(u"故障等级", max_length=30, null=True)
    describe = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Record(models.Model):
    eventitle = models.CharField(u"故障标题", max_length=100, null=True)
    eventstarttime = models.CharField(u"故障开始时间", max_length=100, null=True)
    eventendtime = models.CharField(u"故障结束时间", max_length=100, null=True)
    eventpeople = models.CharField(u"故障责任人", max_length=30, null=True)
    eventclass = models.ForeignKey(Record_list, verbose_name=u"故障等级", on_delete=models.SET_NULL, null=True, blank=True)
    eventproduct = models.CharField(u"影响产品", max_length=30, null=True)
    eventdescribe = models.TextField(u"故障描述", max_length=1000, null=True)
    eventdispose= models.TextField(u"故障改进", max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Faq(models.Model):
    title = models.CharField(u"系统名称", max_length=100, null=True)
    problemclass = models.CharField(u"问题类别", max_length=100, null=True)
    describe = models.TextField(u"问题描述", max_length=2000, null=True)
    solution = models.TextField(u"解决方案", max_length=2000, null=True)
    developername = models.CharField(u"系统开发人员", max_length=30, null=True)
    telephone = models.CharField(u"联系电话", max_length=30, null=True)
    mail= models.CharField(u"邮箱", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Assessment_list(models.Model):
    name = models.CharField(u"考核项", max_length=30, null=True)
    describe = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Assessment(models.Model):
    assessmentname = models.CharField(u"考核人员", max_length=100, null=True)
    assessmentclass = models.ForeignKey(Assessment_list, verbose_name=u"考核项", on_delete=models.SET_NULL, null=True, blank=True)
    assessmentnum = models.TextField(u"考核分值", max_length=2000, null=True)
    assessmentcontent = models.TextField(u"考核内容", max_length=2000, null=True)
    assessmenttime = models.CharField(u"考核时间", max_length=30, null=True)
    recordpersonnel = models.CharField(u"记录人员", max_length=30, null=True)
    remarks= models.CharField(u"备注", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Change(models.Model):
    title = models.CharField(u"变更主题", max_length=50, null=True)
    changetime = models.CharField(u"变更时间", max_length=100, null=True)
    operator = models.CharField(u"操作人", max_length=20, null=True)
    business = models.CharField(u"涉及的业务", max_length=50, null=True)
    content = models.TextField(u"操作内容", max_length=2000, null=True)
    influence = models.CharField(u"影响后果", max_length=100, null=True)
    rollback= models.TextField(u"回滚步骤", max_length=2000, null=True, blank=True)
    recordtime= models.CharField(u"记录时间", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name
