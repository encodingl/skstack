#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from skconfig import views


urlpatterns = [
    url(r'^$', views.index, name='config'),
    url(r'^token/', views.get_token, name='token'),
]