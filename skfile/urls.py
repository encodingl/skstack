#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url,include
from skfile  import views

urlpatterns = [
   url(r'^$',views.index,name="index"),
   url(r'^dir',views.dir,name="dir"),
   url(r'^history',views.history,name="history"),
   url(r'^adddir',views.adddir,name="adddir"),
   url(r'^dir_delete/(?P<ids>\d+)/$',views.dir_delete,name='dir_delete'),
]
