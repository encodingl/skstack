#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from skdomain import views,whitelist

urlpatterns = [
    url(r'^$', views.index, name='domain'),
    url(r'^add/$', views.add, name='add'),
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^delete/(?P<ids>\d+)/$', views.delete, name='delete'),
    url(r'^edit/(?P<ids>\d+)/$', views.edit, name='edit'),
    
    url(r'whitelist/$', whitelist.whitelist, name='whitelist'),
    url(r'^whitelist/add/$', whitelist.whitelist_add, name='whitelist_add'),
    url(r'^whitelist/del/$', whitelist.whitelist_del, name='whitelist_del'),
    url(r'^whitelist/save/$', whitelist.whitelist_save, name='whitelist_save'),
    url(r'^whitelist/edit/(?P<ids>\d+)/$', whitelist.whitelist_edit, name='whitelist_edit'),
]