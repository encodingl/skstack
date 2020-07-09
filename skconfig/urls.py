#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from skconfig import views,inventories



urlpatterns = [
    url(r'^$', views.index, name='config'),
    url(r'^token/', views.get_token, name='token'),
    url(r'^inventories/$', inventories.index, name='inventories'),
    url(r'^flower',views.flower,name='flower'),
]