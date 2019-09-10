#! /usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from skaccounts.models import UserInfo
from lib.type import ASSET_STATUS, MAP_TYPE


class Idc(models.Model):
    name = models.CharField("* 机房名称", max_length=30, null=True)
    address = models.CharField("机房地址", max_length=100, null=True, blank=True)
    tel = models.CharField("机房电话", max_length=30, null=True, blank=True)
    contact = models.CharField("客户经理", max_length=30, null=True, blank=True)
    contact_phone = models.CharField("移动电话", max_length=30, null=True, blank=True)
    jigui = models.CharField("机柜信息", max_length=30, null=True, blank=True)
    ip_range = models.CharField("IP范围", max_length=30, null=True, blank=True)
    bandwidth = models.CharField("接入带宽", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '数据中心'
        verbose_name_plural = verbose_name


class Env(models.Model):
    name = models.CharField("* 环境名称", max_length=30, unique=True)
    address = models.ForeignKey(Idc, verbose_name="所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    descrition = models.CharField("描述", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name


class YwGroup(models.Model):
    name = models.CharField("* 小组名称", max_length=30, unique=True)
    sa = models.CharField("负责人", max_length=30, null=True, blank=True)
    descrition = models.CharField("描述", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name


class MiddleType(models.Model):
    name = models.CharField("* 主机组名称", max_length=30, unique=True)
    descrition = models.CharField("描述", max_length=30, null=True, blank=True)

    def __unicode__(self):
        return self.name


class HostGroup(models.Model):
    name = models.CharField("* 组名", max_length=30, unique=True)
    desc = models.CharField("描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Host(models.Model):
    hostname = models.CharField(max_length=50, verbose_name="* 主机名", unique=True)
    ip = models.GenericIPAddressField("* IP地址", max_length=15, unique=True)
    other_ip = models.CharField("其它IP", max_length=100, null=True, blank=True)
    group = models.ForeignKey(HostGroup, verbose_name="主机分组", on_delete=models.SET_NULL, null=True, blank=True)
    sa = models.ForeignKey(UserInfo, verbose_name="负责人", on_delete=models.SET_NULL, null=True, blank=True)
    env = models.ForeignKey(Env, verbose_name="运行环境", on_delete=models.SET_NULL, null=True, blank=True)
    ywgroup = models.ForeignKey(YwGroup, verbose_name="业务分组", on_delete=models.SET_NULL, null=True, blank=True)
    middletype = models.ForeignKey(MiddleType, verbose_name="主机类型", on_delete=models.SET_NULL, null=True, blank=True)
    asset_no = models.CharField("资产编号", max_length=50, null=True, blank=True)
    status = models.CharField("设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    os = models.CharField("操作系统", max_length=100, null=True, blank=True)
    vendor = models.CharField("设备厂商", max_length=50, null=True, blank=True)
    cpu_model = models.CharField("CPU型号", max_length=100, null=True, blank=True)
    cpu_num = models.CharField("CPU数量", max_length=100, null=True, blank=True)
    memory = models.CharField("内存大小", max_length=30, null=True, blank=True)
    disk = models.CharField("硬盘信息", max_length=255, null=True, blank=True)
    sn = models.CharField("SN号 码", max_length=60, blank=True)
    idc = models.ForeignKey(Idc, verbose_name="所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField("所在位置", max_length=100, null=True, blank=True)
    memo = models.TextField("备注信息", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.hostname


class KafkaTopic(models.Model):
    name = models.CharField(max_length=50, verbose_name="* App名称")
    descrition = models.TextField("备注信息", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name


class App(models.Model):
    name = models.CharField(max_length=50, verbose_name="* APP名称", unique=True)
    ywgroup = models.ForeignKey(YwGroup, verbose_name="业务分组", on_delete=models.SET_NULL, null=True, blank=True)
    sa = models.ForeignKey(UserInfo, verbose_name="运维负责人", on_delete=models.SET_NULL, null=True, blank=True)
    env = models.ForeignKey(Env, verbose_name="运行环境", on_delete=models.SET_NULL, null=True, blank=True)
    belong_ip = models.ManyToManyField(Host, verbose_name="所属主机", blank=True)
    kafka = models.ManyToManyField(KafkaTopic, verbose_name="Kafka列表", blank=True)
    web_port = models.IntegerField(verbose_name="Web端口号", null=True, blank=True)
    dubbo_port = models.IntegerField(verbose_name="Dubbo端口号", null=True, blank=True)
    status = models.CharField("设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    descrition = models.TextField("备注信息", max_length=200, null=True, blank=True)

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
    price = models.IntegerField(verbose_name='价格')

    def __unicode__(self):
        return self.name


class DbSource(models.Model):
    name = models.CharField(max_length=30, verbose_name="* 名称", unique=True)
    host = models.GenericIPAddressField(max_length=30, verbose_name="主机ip", null=True)
    user = models.CharField(max_length=30, verbose_name="用户名", null=True, blank=True)
    password = models.CharField(max_length=30, verbose_name="密码", null=True, blank=True)
    port = models.IntegerField(default=3306, verbose_name="端口号", null=True, blank=True)
    db = models.CharField(max_length=30, verbose_name="数据库名", null=True, blank=True)

    def __unicode__(self):
        return self.user


class WhileIp(models.Model):
    ip = models.CharField(max_length=50, verbose_name="* 白名单", unique=True)
    name = models.CharField(max_length=50, verbose_name="名称", null=True, blank=True)
    descrition = models.TextField("用途", max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.ip


class Url(models.Model):
    name = models.CharField(max_length=50, verbose_name="* Url名称", unique=True)
    nickname = models.CharField(max_length=50, verbose_name="业务名称", null=True, blank=True)
    whitelist = models.ManyToManyField(WhileIp, verbose_name="白名单列表", blank=True)
    mapip = models.GenericIPAddressField(max_length=50, verbose_name="映射IP", null=True, blank=True)
    type = models.CharField("类型", choices=MAP_TYPE, max_length=30, null=True, blank=True)
    ywgroup = models.ForeignKey(YwGroup, verbose_name="业务分组", on_delete=models.SET_NULL, null=True, blank=True)
    sa = models.ForeignKey(UserInfo, verbose_name="运维负责人", on_delete=models.SET_NULL, null=True, blank=True)
    env = models.ForeignKey(Env, verbose_name="运行环境", on_delete=models.SET_NULL, null=True, blank=True)
    belongapp = models.ForeignKey(App, verbose_name="所属App", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField("设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    descrition = models.TextField("用途", max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.name
