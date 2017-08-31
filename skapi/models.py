#coding:utf8
from __future__ import unicode_literals

from datetime import datetime
from django.db import models

# Create your models here.



class Test(models.Model):
    name = models.CharField(max_length=30)
    vendor = models.CharField(max_length=30,null=True)
    bandwidth = models.CharField(max_length=30,null=True)
    tel = models.CharField(max_length=30,null=True)
    contact = models.CharField(max_length=30,null=True)
    price = models.IntegerField(verbose_name=u'价格',null=True)

    def __unicode__(self):
        return self.name
    class Meta:
        app_label = "skapi"