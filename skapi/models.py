#coding:utf8
from __future__ import unicode_literals
from django.db import models


class UserList(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"* 主机名", unique=True)
    descrition = models.TextField(u"备注信息", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name