#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url,include
from skfile  import views

urlpatterns = [
   url(r'file',views.index,name="file"),
   url(r'^dirmanager',views.dir,name="dirmanager"),
   url(r'^fhistory',views.file_history,name="fhistory"),
   url(r'^dir_add',views.adddir,name="dir_add"),
]
