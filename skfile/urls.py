#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url,include
from skfile  import views

urlpatterns = [
   url(r'^skfile',views.index,name="skfile"),
   url(r'^dir',views.dir,name="dir"),
   url(r'^file_history',views.file_history,name="file_history"),
   url(r'^adddir',views.adddir,name="adddir"),
]
