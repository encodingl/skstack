from __future__ import unicode_literals

from datetime import datetime
from django.db import models

# Create your models here.


class AppGroup(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=100, null=True)


class App_SA(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=100, null=True)


class Applist(models.Model):
    name = models.CharField(max_length=30,unique=True)
    alias_name = models.CharField(max_length=50,null=True)
    is_active = models.BooleanField(default=True)
    sa = models.ForeignKey(App_SA, null=True)
    group = models.ForeignKey(AppGroup, null=True)
    #created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name