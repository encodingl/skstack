# coding:utf8
from __future__ import unicode_literals
from django.db import models
from skcmdb.models import App


class AlarmUser(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* 告警收件人", unique=True)
    email = models.EmailField(max_length=255, verbose_name=u"* 邮箱", null=True)
    tel = models.CharField(max_length=50, verbose_name=u"* 电话号码", null=True)
    dd = models.CharField(max_length=50, verbose_name=u"* 钉钉号", null=True)
    app = models.ManyToManyField(App, verbose_name=u"授权APP", blank=True)

    def __unicode__(self):
        return self.name


class AlarmGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* 告警分组名称", unique=True)
    serial = models.CharField(max_length=20,default='0', verbose_name=u"微信编号", null=True, blank=True)
    tel_status = models.IntegerField(default=0, verbose_name=u"电话状态")
    user = models.ManyToManyField(AlarmUser, verbose_name=u"告警名单", blank=True)
    descrition = models.TextField(max_length=200, verbose_name=u"监控范围", null=True, blank=True)

    def __unicode__(self):
        return self.name


class AlarmList(models.Model):
    name = models.ForeignKey(AlarmUser, verbose_name=u"所属用户", on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(AlarmGroup, verbose_name=u"所属分组", on_delete=models.SET_NULL, null=True, blank=True)
    weixin_status = models.BooleanField(default=False, verbose_name=u"微信状态")
    email_status = models.BooleanField(default=False, verbose_name=u"邮件状态")
    sms_status = models.BooleanField(default=False, verbose_name=u"短信状态")
    dd_status = models.BooleanField(default=False, verbose_name=u"钉钉状态")

    def __unicode__(self):
        return self.name.name


class TokenAuth(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* 授权用户", unique=True)
    token = models.CharField(max_length=50, verbose_name=u"* Token", null=True)
    descrition = models.CharField(max_length=50, verbose_name=u"用途", null=True, blank=True)

    def __unicode__(self):
        return self.name
