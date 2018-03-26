# coding:utf8
from __future__ import unicode_literals
from django.db import models
import django.utils.timezone as timezone
from lib.type import Alarm_TYPE
from skcmdb.models import App
from skaccounts.models import UserInfo


class UserPolicy(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"* 策略名称", null=True, unique=True)
    weixin_status = models.BooleanField(default=False, verbose_name=u"微信状态")
    email_status = models.BooleanField(default=False, verbose_name=u"邮件状态")
    sms_status = models.BooleanField(default=False, verbose_name=u"短信状态")
    dd_status = models.BooleanField(default=False, verbose_name=u"钉钉状态")
    tel_status = models.BooleanField(default=False, verbose_name=u"电话状态")

    def __unicode__(self):
        return self.name


class AlarmUser(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"* 姓名", unique=True)
    email = models.EmailField(max_length=30, verbose_name=u"* 邮箱", null=True)
    tel = models.CharField(max_length=20, verbose_name=u"* 电话号码", null=True)
    dd = models.CharField(max_length=20, verbose_name=u"* 钉钉号", null=True)
    policy = models.ForeignKey(UserPolicy, verbose_name=u"* 用户策略", on_delete=models.SET_NULL, null=True)
    app = models.ManyToManyField(App, verbose_name=u"授权APP", blank=True)

    def __unicode__(self):
        return self.name


class TokenAuth(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"* 名称", unique=True)
    token = models.CharField(max_length=20, verbose_name=u"* Token", null=True)
    descrition = models.CharField(max_length=50, verbose_name=u"用途", null=True, blank=True)

    def __unicode__(self):
        return self.name


class LevelPolicy(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"* 策略名称", null=True, unique=True)
    info_status = models.BooleanField(default=False, verbose_name=u"Info级别")
    warn_status = models.BooleanField(default=False, verbose_name=u"Warn级别")
    error_status = models.BooleanField(default=False, verbose_name=u"Error级别")
    fatal_status = models.BooleanField(default=False, verbose_name=u"Fatal级别")

    def __unicode__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField(u"业务名称", max_length=20, null=True)
    typecode = models.CharField(u"业务编码", max_length=10, null=True)
    descrition = models.TextField(u"描述", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name


class AlarmGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* 分组名称", unique=True)
    serial = models.IntegerField(default=0, verbose_name=u"微信通道", blank=True)
    servicetype = models.ForeignKey(ServiceType, verbose_name=u"服务类型", null=True, blank=True)
    levelpolicy = models.ForeignKey(LevelPolicy, verbose_name=u"日志策略", null=True, blank=True)
    user = models.ManyToManyField(UserInfo, verbose_name=u"告警名单", blank=True)
    tokens = models.ManyToManyField(TokenAuth, verbose_name=u"授权Token", blank=True)
    descrition = models.TextField(max_length=200, verbose_name=u"详细描述", default='', blank=True)

    def __unicode__(self):
        return self.name


class AlarmList(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name=u"用户ID", on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(AlarmGroup, verbose_name=u"所属分组", on_delete=models.SET_NULL, null=True)
    weixin_status = models.BooleanField(default=False, verbose_name=u"微信状态")
    email_status = models.BooleanField(default=False, verbose_name=u"邮件状态")
    sms_status = models.BooleanField(default=False, verbose_name=u"短信状态")
    dd_status = models.BooleanField(default=False, verbose_name=u"钉钉状态")
    tel_status = models.BooleanField(default=False, verbose_name=u"电话状态")
    app = models.ManyToManyField(App, verbose_name=u"授权APP", blank=True)

    def __unicode__(self):
        return self.user.nickname


class AlarmRecord(models.Model):
    name = models.CharField(u"发送", max_length=10, null=True)
    create_time = models.DateTimeField(u'保存日期', default=timezone.now)
    token = models.CharField(u"授权Token", max_length=20, null=True)
    type = models.CharField(u"类型", choices=Alarm_TYPE, max_length=20, null=True)
    receiver = models.CharField(u"接收人", max_length=50, null=True)
    serial = models.CharField(u"微信通道", max_length=10, null=True)
    level = models.CharField(u"级别", max_length=10, null=True)
    subject = models.TextField(u"标题", max_length=50, null=True)
    content = models.TextField(u"内容", max_length=200, null=True)

    def __unicode__(self):
        return self.name


class ZabbixRecord(models.Model):
    name = models.CharField(u"发送者", max_length=10, null=True)
    create_time = models.DateTimeField(u'记录时间', default=timezone.now)
    token = models.CharField(u"授权Token", max_length=20, null=True)
    appname = models.CharField(u"APPNAME", max_length=50, null=True)
    subject = models.TextField(u"标题", max_length=50, null=True)
    status = models.CharField(u"状态", max_length=30, null=True)
    host = models.CharField(u"主机", max_length=30, null=True)
    event = models.CharField(u"事件ID", max_length=30, null=True)
    content = models.TextField(u"内容", max_length=200, null=True)

    def __unicode__(self):
        return self.name
