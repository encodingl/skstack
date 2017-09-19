#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from skaccounts.models import UserInfo

ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
)

MAP_TYPE = (
    (str(1), u"外网"),
    (str(2), u"内网"),
)


class Idc(models.Model):
    name = models.CharField(u"* 机房名称", max_length=30, null=True)
    address = models.CharField(u"机房地址", max_length=100, null=True, blank=True)
    tel = models.CharField(u"机房电话", max_length=30, null=True, blank=True)
    contact = models.CharField(u"客户经理", max_length=30, null=True, blank=True)
    contact_phone = models.CharField(u"移动电话", max_length=30, null=True, blank=True)
    jigui = models.CharField(u"机柜信息", max_length=30, null=True, blank=True)
    ip_range = models.CharField(u"IP范围", max_length=30, null=True, blank=True)
    bandwidth = models.CharField(u"接入带宽", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'数据中心'
        verbose_name_plural = verbose_name


class Env(models.Model):
    name = models.CharField(u"* 环境名称", max_length=30, unique=True)
    address = models.ForeignKey(Idc, verbose_name=u"所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    descrition = models.CharField(u"描述", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name


class YwGroup(models.Model):
    name = models.CharField(u"* 小组名称", max_length=30, unique=True)
    sa = models.CharField(u"负责人", max_length=30, null=True, blank=True)
    descrition = models.CharField(u"描述", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name


class MiddleType(models.Model):
    name = models.CharField(u"* 主机组名称", max_length=30, unique=True)
    descrition = models.CharField(u"描述", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name


class HostGroup(models.Model):
    name = models.CharField(u"* 组名", max_length=30, unique=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Host(models.Model):
    hostname = models.CharField(max_length=50, verbose_name=u"* 主机名", unique=True)
    ip = models.GenericIPAddressField(u"* IP地址", max_length=15, unique=True)
    other_ip = models.CharField(u"其它IP", max_length=100, null=True, blank=True)
    group = models.ForeignKey(HostGroup, verbose_name=u"主机分组", on_delete=models.SET_NULL, null=True, blank=True)
    sa = models.ForeignKey(UserInfo, verbose_name=u"负责人", on_delete=models.SET_NULL, null=True, blank=True)
    env = models.ForeignKey(Env, verbose_name=u"运行环境", on_delete=models.SET_NULL, null=True, blank=True)
    ywgroup = models.ForeignKey(YwGroup, verbose_name=u"业务分组", on_delete=models.SET_NULL, null=True, blank=True)
    middletype = models.ForeignKey(MiddleType, verbose_name=u"主机类型", on_delete=models.SET_NULL, null=True, blank=True)
    asset_no = models.CharField(u"资产编号", max_length=50, null=True, blank=True)
    status = models.CharField(u"设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    os = models.CharField(u"操作系统", max_length=100, null=True, blank=True)
    vendor = models.CharField(u"设备厂商", max_length=50, null=True, blank=True)
    cpu_model = models.CharField(u"CPU型号", max_length=100, null=True, blank=True)
    cpu_num = models.CharField(u"CPU数量", max_length=100, null=True, blank=True)
    memory = models.CharField(u"内存大小", max_length=30, null=True, blank=True)
    disk = models.CharField(u"硬盘信息", max_length=255, null=True, blank=True)
    sn = models.CharField(u"SN号 码", max_length=60, blank=True)
    idc = models.ForeignKey(Idc, verbose_name=u"所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(u"所在位置", max_length=100, null=True, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.hostname


class KafkaTopic(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* App名称")
    descrition = models.TextField(u"备注信息", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name


class App(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* APP名称", unique=True)
    ywgroup = models.ForeignKey(YwGroup, verbose_name=u"业务分组", on_delete=models.SET_NULL, null=True, blank=True)
    sa = models.ForeignKey(UserInfo, verbose_name=u"运维负责人", on_delete=models.SET_NULL, null=True, blank=True)
    env = models.ForeignKey(Env, verbose_name=u"运行环境", on_delete=models.SET_NULL, null=True, blank=True)
    belong_ip = models.ManyToManyField(Host, verbose_name=u"所属主机", blank=True)
    kafka = models.ManyToManyField(KafkaTopic, verbose_name=u"Kafka列表", blank=True)
    web_port = models.IntegerField(verbose_name=u"Web端口号", null=True, blank=True)
    dubbo_port = models.IntegerField(verbose_name=u"Dubbo端口号", null=True, blank=True)
    status = models.CharField(u"设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    descrition = models.TextField(u"备注信息", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name


class IpSource(models.Model):
    net = models.CharField(max_length=30)
    subnet = models.CharField(max_length=30, null=True)
    describe = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.net


class InterFace(models.Model):
    name = models.CharField(max_length=30)
    vendor = models.CharField(max_length=30, null=True)
    bandwidth = models.CharField(max_length=30, null=True)
    tel = models.CharField(max_length=30, null=True)
    contact = models.CharField(max_length=30, null=True)
    startdate = models.DateField()
    enddate = models.DateField()
    price = models.IntegerField(verbose_name=u'价格')

    def __unicode__(self):
        return self.name


class DbSource(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"* 名称", unique=True)
    host = models.GenericIPAddressField(max_length=30, verbose_name=u"主机ip", null=True)
    user = models.CharField(max_length=30, verbose_name=u"用户名", null=True, blank=True)
    password = models.CharField(max_length=30, verbose_name=u"密码", null=True, blank=True)
    port = models.IntegerField(default=3306, verbose_name=u"端口号", null=True, blank=True)
    db = models.CharField(max_length=30, verbose_name=u"数据库名", null=True, blank=True)

    def __unicode__(self):
        return self.user


class Url(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* Url名称", unique=True)
    nickname = models.CharField(max_length=50, verbose_name=u"业务名称", null=True, blank=True)
    whitelist = models.CharField(max_length=50, verbose_name=u"白名单列表", null=True, blank=True)
    mapip = models.GenericIPAddressField(max_length=50, verbose_name=u"映射IP", null=True, blank=True)
    type = models.CharField(u"类型", choices=MAP_TYPE, max_length=30, null=True, blank=True)
    sa = models.ForeignKey(UserInfo, verbose_name=u"运维负责人", on_delete=models.SET_NULL, null=True, blank=True)
    env = models.ForeignKey(Env, verbose_name=u"运行环境", on_delete=models.SET_NULL, null=True, blank=True)
    belongapp = models.ForeignKey(App, verbose_name=u"所属App", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(u"设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    descrition = models.TextField(u"用途", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name
