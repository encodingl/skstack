#! /usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from skaccounts.models import UserInfo
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

TRACK_STATUS = (
    (str(0), "已解决"),
    (str(1), "跟进中"),
    (str(2), "未解决"),
    )


class Record_list(models.Model):
    name = models.CharField("故障等级", max_length=30, null=True)
    describe = models.CharField("描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Record(models.Model):
    eventitle = models.CharField("故障标题", max_length=100, null=True)
    eventstarttime = models.CharField("故障开始时间", max_length=100, null=True)
    eventendtime = models.CharField("故障结束时间", max_length=100, null=True)
    eventpeople = models.CharField("故障责任人", max_length=30, null=True)
    eventclass = models.ForeignKey(Record_list, verbose_name="故障等级", on_delete=models.SET_NULL, null=True, blank=True)
    eventproduct = models.CharField("影响产品", max_length=30, null=True)
    eventdescribe = models.TextField("故障描述", max_length=1000, null=True)
    eventdispose= models.TextField("故障改进", max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Track_list(models.Model):
    name = models.CharField("名称", max_length=30, null=True)
    describe = models.CharField("描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Track(models.Model):
    title = models.CharField("标题", max_length=100, null=True)
    trackclass = models.ForeignKey(Track_list, verbose_name="分类", on_delete=models.SET_NULL, null=True, blank=True)
    trackdescribe = models.TextField("问题描述", max_length=1000, null=True)
    trackdispose = models.TextField("改进方法", max_length=1000, null=True, blank=True)
   # tracktime = models.CharField(u"记录时间", max_length=100, null=True)
    user = models.CharField(editable=False, max_length=100, null=True)
    #status = models.BooleanField(default=False, verbose_name=u"解决状态")
    status = models.CharField("解决状态", choices=TRACK_STATUS, max_length=30, null=True, blank=True)
    tracktime = models.DateTimeField("记录时间", auto_now=True)
    remarks = models.CharField("备注", max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Faq_list(models.Model):
    name = models.CharField("问题分类", max_length=30, null=True)
    describe = models.CharField("描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Faq(models.Model):
    title = models.CharField("问题标题", max_length=100, null=True)
    #problemclass = models.CharField(u"问题类别", max_length=100, null=True)
    problemclass = models.ForeignKey(Faq_list, verbose_name="问题分类", on_delete=models.SET_NULL, null=True, blank=True)
    #describe = models.TextField(u"问题描述", max_length=2000, null=True)
    describe = RichTextUploadingField(verbose_name="问题描述", max_length=2000, null=True)
    #solution = models.TextField(u"解决方案", max_length=2000, null=True)
    solution = RichTextUploadingField(verbose_name="解决方案", max_length=2000, null=True)
    user =  models.CharField(editable=False, max_length=100, null=True)

    def __unicode__(self):
        return self.name

class Assessment_list(models.Model):
    name = models.CharField("类型", max_length=30, null=True)
    describe = models.CharField("描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Assessment(models.Model):
    assessmentname = models.CharField("对象", max_length=100, null=True)
    assessmentclass = models.ForeignKey(Assessment_list, verbose_name="类型", on_delete=models.SET_NULL, null=True, blank=True)
    assessmentnum = models.TextField("权重", max_length=2000, null=True)
    assessmentcontent = models.TextField("内容", max_length=2000, null=True)
    assessmenttime = models.CharField("时间", max_length=30, null=True)
    recordpersonnel = models.CharField("记录人员", max_length=30, null=True)
    remarks= models.CharField("备注", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Change(models.Model):
    title = models.CharField("变更主题", max_length=50, null=True)
    changetime = models.CharField("变更时间", max_length=100, null=True)
    operator = models.CharField("操作人", max_length=20, null=True)
    business = models.CharField("涉及的业务", max_length=50, null=True)
    content = models.TextField("操作内容", max_length=2000, null=True)
    influence = models.CharField("影响后果", max_length=100, null=True)
    rollback= models.TextField("回滚步骤", max_length=2000, null=True, blank=True)
    recordtime= models.CharField("记录时间", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Memo(models.Model):
    title = models.CharField("标题", max_length=50, null=True)
    content = models.TextField("内容", max_length=2000, null=True)
    noticetime = models.DateField("通知时间", max_length=100, null=True)
    expirationtime = models.DateField("到期时间", max_length=100, null=True)
    mail = models.EmailField("通知邮箱",max_length=200, null=True)
    recordtime = models.DateTimeField("记录时间", auto_now=True)
    user = models.CharField(editable=False, max_length=100, null=True)

    def __unicode__(self):
        return self.name
