# coding:utf8
from __future__ import unicode_literals
from django.db import models


class AlarmUser(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* 告警收件人", unique=True)
    email = models.EmailField(max_length=255, verbose_name=u"* 邮箱", null=True)
    tel = models.CharField(max_length=50, verbose_name=u"* 电话号码", null=True)
    dd = models.CharField(max_length=50, verbose_name=u"* 钉钉号", null=True)

    def __unicode__(self):
        return self.name

class AlarmGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* 告警分组名称", unique=True)
    serial = models.IntegerField(default=0, verbose_name=u"微信编号", null=True, blank=True)
    tel_status = models.IntegerField(default=0,verbose_name=u"电话状态")
    user = models.ManyToManyField(AlarmUser, verbose_name=u"告警名单", blank=True)
    descrition = models.CharField(max_length=50, verbose_name=u"描述", null=True, blank=True)

    def __unicode__(self):
        return self.name


class AlarmList(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"所属用户", null=True, blank=True)
    group = models.CharField(max_length=50, verbose_name=u"所属分组", null=True, blank=True)
    weixin_status = models.BooleanField(default=False,verbose_name=u"微信状态")
    email_status = models.BooleanField(default=False,verbose_name=u"邮件状态")
    sms_status = models.BooleanField(default=False,verbose_name=u"短信状态")
    dd_status = models.BooleanField(default=False,verbose_name=u"钉钉状态")

    def __unicode__(self):
        return self.name

class AlarmStatus(models.Model):
    weixin_status = models.BooleanField(default=False,verbose_name=u"微信状态")
    email_status = models.BooleanField(default=False,verbose_name=u"邮件状态")
    sms_status = models.BooleanField(default=False,verbose_name=u"短信状态")
    dd_status = models.BooleanField(default=False,verbose_name=u"钉钉状态")
    tel_status = models.BooleanField(default=False, verbose_name=u"钉钉状态")

    def __unicode__(self):
        return self.name