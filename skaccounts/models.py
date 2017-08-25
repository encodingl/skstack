#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from sktask.models import job

# Create your models here.
AuditFlow_LEVEL = (
    (str(1), u"一层审核"),
    (str(2), u"二层审核"),
    (str(3), u"三层审核"),
    )

class PermissionList(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.url)


class RoleList(models.Model):
    name = models.CharField(max_length=64)
    # permission = models.ManyToManyField(PermissionList, null=True, blank=True)
    permission = models.ManyToManyField(PermissionList, blank=True)

    def __unicode__(self):
        return self.name
    
class RoleJob(models.Model):
    name = models.CharField(max_length=64)
    # permission = models.ManyToManyField(PermissionList, null=True, blank=True)
    permission = models.ManyToManyField(job, blank=True)

    def __unicode__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email,
            username=username,
            password=password,
        )

        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserGroup(models.Model):
    name = models.CharField(max_length=64)    # permission = models.ManyToManyField(PermissionList, null=True, blank=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name
    
class UserInfo(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField(max_length=64, null=True)
    type = models.IntegerField(null=True)
    role = models.ForeignKey(RoleList, null=True, blank=True)
    role_job = models.ForeignKey(RoleJob, null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    #usergroup = models.ManyToManyField(UserGroup,null=True,blank=True)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
    # def __unicode__(self):
    #     return self.nickname

class AuditFlow(models.Model):
    name = models.CharField(u"登录用户",max_length=50)
    level = models.CharField(u"审核层级", choices=AuditFlow_LEVEL, max_length=10, null=True, blank=True)
    l1 = models.ForeignKey(UserGroup, verbose_name=u"第1级审核用户组", on_delete=models.SET_NULL, null=True, blank=True,related_name='l1')
    l2 = models.ForeignKey(UserGroup, verbose_name=u"第2级审核用户组", on_delete=models.SET_NULL, null=True, blank=True,related_name='l2')
    l3 = models.ForeignKey(UserGroup, verbose_name=u"第3级审核用户组", on_delete=models.SET_NULL, null=True, blank=True,related_name='l3')
    def __unicode__(self):
        return self.name
