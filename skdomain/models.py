#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.db import models

NAVI_STATUS = (
    (str(0), u"未启用"),
    (str(1), u"启用"),
    (str(2), u"已下线"),
    )
class WhiteList(models.Model):
    ip = models.GenericIPAddressField(u"IP", max_length=15)
    description = models.CharField(u"描述",max_length=50)
    
    
    def __unicode__(self):
        return self.ip
    
class navi(models.Model):
    name = models.CharField(u"名称",max_length=50)
    description = models.CharField(u"描述",max_length=50)
    url = models.URLField(u"网址")
    online_status = models.CharField(u"online_status", choices=NAVI_STATUS, max_length=30, null=True, blank=True)
    white_list = models.ManyToManyField(WhiteList, verbose_name=u"白名单", blank=True)
    
    def __unicode__(self):
        return self.name