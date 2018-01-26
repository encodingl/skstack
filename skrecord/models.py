#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


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

class Track_list(models.Model):
    name = models.CharField(u"名称", max_length=30, null=True)
    describe = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(u"标题", max_length=100, null=True)
    trackclass = models.ForeignKey(Track_list, verbose_name=u"分类", on_delete=models.SET_NULL, null=True, blank=True)
    trackdescribe = models.TextField(u"问题描述", max_length=1000, null=True)
    trackdispose = models.TextField(u"改进方法", max_length=1000, null=True, blank=True)
   # tracktime = models.CharField(u"记录时间", max_length=100, null=True)
    tracktime = models.DateTimeField(u"记录时间", auto_now=True)
    remarks = models.CharField(u"备注", max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Faq_list(models.Model):
    name = models.CharField(u"问题分类", max_length=30, null=True)
    describe = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Faq(models.Model):
    title = models.CharField(u"问题标题", max_length=100, null=True)
    #problemclass = models.CharField(u"问题类别", max_length=100, null=True)
    problemclass = models.ForeignKey(Faq_list, verbose_name=u"问题分类", on_delete=models.SET_NULL, null=True, blank=True)
    describe = models.TextField(u"问题描述", max_length=2000, null=True)
    solution = models.TextField(u"解决方案", max_length=2000, null=True)

    def __unicode__(self):
        return self.name

class Assessment_list(models.Model):
    name = models.CharField(u"类型", max_length=30, null=True)
    describe = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Assessment(models.Model):
    assessmentname = models.CharField(u"对象", max_length=100, null=True)
    assessmentclass = models.ForeignKey(Assessment_list, verbose_name=u"类型", on_delete=models.SET_NULL, null=True, blank=True)
    assessmentnum = models.TextField(u"权重", max_length=2000, null=True)
    assessmentcontent = models.TextField(u"内容", max_length=2000, null=True)
    assessmenttime = models.CharField(u"时间", max_length=30, null=True)
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
