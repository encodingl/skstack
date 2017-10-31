#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url,include
from skyw import views,rota,notice,platform,event

urlpatterns = [
    url(r'^$',views.index,name='yw'),
    url(r'^list', views.list, name='list'),
    url(r'^add', views.add, name='add'),
    url(r'^rota_add', rota.rota_add, name='rota_add'),
    url(r'^notice_add', notice.notice_add, name='notice_add'),
    url(r'^event_add',event.event_add, name='event_add'),

    url(r'^edit/(?P<ids>\d+)/$', views.edit,name='edit'),
    url(r'^rota_edit/(?P<ids>\d+)/$', rota.rota_edit, name='rota_edit'),
    url(r'^notice_edit/(?P<ids>\d+)/$', notice.notice_edit, name='notice_edit'),
    url(r'^event_edit/(?P<ids>\d+)/$', event.event_edit, name='event_edit'),

    url(r'^delete/(?P<ids>\d+)/$',views.delete,name='delete'),
    url(r'^notice_delete/(?P<ids>\d+)/$', notice.notice_delete, name='notice_delete'),
    url(r'^rota_delete/(?P<ids>\d+)/$',rota.rota_delete,name='rota_delete'),
    url(r'^event_delete/(?P<ids>\d+)/$',event.event_delete,name='event_delete'),

    #platform 运维平台
    url(r'^platform_index',platform.platform_list,name='platform_index'),
    url(r'^platform_list',platform.platform_list,name='platform_list'),
    url(r'^platform_add',platform.platform_add,name='platform_add'),
    url(r'^platformclass_add',platform.platformclass_add,name='platformclass_add'),
    url(r'^platform_edit/(?P<ids>\d+)/$', platform.platform_edit, name='platform_edit'),
    url(r'^platform_delete/(?P<ids>\d+)/$',platform.platform_delete,name='platform_delete'),
    url(r'^platformclass_edit/(?P<ids>\d+)/$', platform.platformclass_edit, name='platformclass_edit'),
    url(r'^platformclass_delete/(?P<ids>\d+)/$', platform.platformclass_delete, name='platformclass_delete'),
]
