#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url,include
from skyw import views,rota,notice,platform,event

urlpatterns = [
    url(r'^nav/$',views.daohang,name='yw'),
    url(r'^nav/dutyuser/$', views.dutyuser, name='dutyuser'),
    url(r'^nav/dutyinfo/$', rota.dutyinfo, name='dutyinfo'),
    url(r'^nav/notify/$', notice.notify, name='notify'),
    url(r'^nav/ywevent/$', event.ywevent, name='ywevent'),
    url(r'^nav/platclass/$', platform.platclass, name='platclass'),
    url(r'^nav/plat/$', platform.plat, name='plat'),
    # url(r'^list', views.index, name='list'),
    url(r'^nav/yw_add/$', views.add, name='yw_add'),
    url(r'^nav/rota_add/$', rota.rota_add, name='rota_add'),
    url(r'^nav/notice_add/$', notice.notice_add, name='notice_add'),
    url(r'^nav/event_add/$',event.event_add, name='event_add'),

    url(r'^nav/yw_edit/(?P<ids>\d+)/$',views.yw_edit, name='yw_edit'),
    url(r'^nav/rota_edit/(?P<ids>\d+)/$', rota.rota_edit, name='rota_edit'),
    url(r'^nav/notice_edit/(?P<ids>\d+)/$', notice.notice_edit, name='notice_edit'),
    url(r'^nav/event_edit/(?P<ids>\d+)/$', event.event_edit, name='event_edit'),

    url(r'^nav/delete/(?P<ids>\d+)/$',views.delete,name='yw_delete'),
    url(r'^nav/notice_delete/(?P<ids>\d+)/$', notice.notice_delete, name='notice_delete'),
    url(r'^nav/rota_delete/(?P<ids>\d+)/$',rota.rota_delete,name='rota_delete'),
    url(r'^nav/event_delete/(?P<ids>\d+)/$',event.event_delete,name='event_delete'),

    #platform 运维平台
    url(r'^nav/platform_add',platform.platform_add,name='platform_add'),
    url(r'^nav/platformclass_add',platform.platformclass_add,name='platformclass_add'),
    url(r'^nav/platform_edit/(?P<ids>\d+)/$', platform.platform_edit, name='platform_edit'),
    url(r'^nav/platform_delete/(?P<ids>\d+)/$',platform.platform_delete,name='platform_delete'),
    url(r'^nav/platformclass_edit/(?P<ids>\d+)/$', platform.platformclass_edit, name='platformclass_edit'),
    url(r'^nav/platformclass_delete/(?P<ids>\d+)/$', platform.platformclass_delete, name='platformclass_delete'),
]
