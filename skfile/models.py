#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from __future__ import unicode_literals
from django.db import models

class Dirmanager(models.Model):
       dirname=models.CharField(u"配置文件目录", max_length=30, null=True,unique=True)

       def __unicode__(self):
           return self.dirname
