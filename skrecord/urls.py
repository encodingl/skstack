
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url,include
#from . import views
from skrecord import views,record_list,faq,assessment,assessment_list,change

urlpatterns = [
    #url(r'^$', views.index, name='record'),
    url(r'^record/$', views.index, name='record'),
    url(r'^add/$', views.add, name='add'),
    url(r'^delete/(?P<ids>\d+)/$', views.delete, name='delete'),
    url(r'^edit/(?P<ids>\d+)/$', views.edit, name='edit'),
    url(r'^record/add/$', views.add, name='record_add'),
    url(r'^record/del/$', views.delete, name='record_del'),
    url(r'^record/save/$', views.message, name='record_message'),
    url(r'^record/edit/(?P<ids>\d+)/$', views.edit, name='record_edit'),
    url(r'^record/detail/(?P<ids>\d+)/$', views.detail, name='record_detail'),

    url(r'^record_list/$', record_list.record_list, name='record_list'),
    url(r'^add/$', record_list.add, name='add'),
    url(r'^record_list/delete/(?P<ids>\d+)/$', record_list.record_list_delete, name='record_list_delete'),
    url(r'^edit/(?P<ids>\d+)/$', record_list.edit, name='edit'),
    url(r'^record_list/add/$', record_list.add, name='record_list_add'),
    url(r'^arecord_list/save/$', record_list.message, name='arecord_list_message'),
    url(r'^record_list/edit/(?P<ids>\d+)/$', record_list.edit, name='record_list_edit'),
    url(r'^record_list/detail/(?P<ids>\d+)/$', record_list.detail, name='record_list_detail'),

    url(r'^faq/$', faq.faq, name='faq'),
    url(r'^add/$', faq.add, name='add'),
    url(r'^faq/delete/(?P<ids>\d+)/$', faq.faq_delete, name='faq_delete'),
    url(r'^edit/(?P<ids>\d+)/$', faq.edit, name='edit'),
    url(r'^faq/add/$', faq.add, name='faq_add'),
    #url(r'^faq/del/$', faq.faq_del, name='faq_del'),
    url(r'^faq/save/$', faq.message, name='faq_message'),
    url(r'^faq/edit/(?P<ids>\d+)/$', faq.edit, name='faq_edit'),
    url(r'^faq/detail/(?P<ids>\d+)/$', faq.detail, name='faq_detail'),

    url(r'^assessment/$', assessment.assessment, name='assessment'),
    url(r'^add/$', assessment.add, name='add'),
    url(r'^assessment/delete/(?P<ids>\d+)/$', assessment.assessment_delete, name='assessment_delete'),
    url(r'^edit/(?P<ids>\d+)/$', assessment.edit, name='edit'),
    url(r'^assessment/add/$', assessment.add, name='assessment_add'),
    url(r'^assessment/save/$', assessment.message, name='assessment_message'),
    url(r'^assessment/edit/(?P<ids>\d+)/$', assessment.edit, name='assessment_edit'),
    url(r'^assessment/detail/(?P<ids>\d+)/$', assessment.detail, name='assessment_detail'),

    url(r'^assessment_list/$', assessment_list.assessment_list, name='assessment_list'),
    url(r'^add/$', assessment_list.add, name='add'),
    url(r'^assessment_list/delete/(?P<ids>\d+)/$', assessment_list.assessment_list_delete, name='assessment_list_delete'),
    url(r'^edit/(?P<ids>\d+)/$', assessment_list.edit, name='edit'),
    url(r'^assessment_list/add/$', assessment_list.add, name='assessment_list_add'),
    url(r'^assessment_list/save/$', assessment_list.message, name='assessment_list_message'),
    url(r'^assessment_list/edit/(?P<ids>\d+)/$', assessment_list.edit, name='assessment_list_edit'),
    url(r'^assessment_list/detail/(?P<ids>\d+)/$', assessment_list.detail, name='assessment_list_detail'),

    url(r'^change/$', change.change, name='change'),
    url(r'^add/$', change.add, name='add'),
    url(r'^change/delete/(?P<ids>\d+)/$', change.change_delete, name='change_delete'),
    #url(r'^edit/(?P<ids>\d+)/$', change.edit, name='edit'),
    url(r'^change/add/$', change.add, name='change_add'),
    url(r'^change/save/$', change.message, name='change_message'),
    url(r'^change/edit/(?P<ids>\d+)/$', change.edit, name='change_edit'),
    url(r'^change/detail/(?P<ids>\d+)/$', change.detail, name='change_detail'),
]
