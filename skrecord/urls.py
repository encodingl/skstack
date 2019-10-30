
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
#from . import views
from skrecord import views,record_list,faq,faq_list,assessment,assessment_list,change,track,track_list,memo


urlpatterns = [
    url(r'^record/$', views.index, name='record'),
    url(r'^delete/(?P<ids>\d+)/$', views.delete, name='delete'),
    url(r'^edit/(?P<ids>\d+)/$', views.edit, name='edit'),
    url(r'^record/add/$', views.add, name='record_add'),
    url(r'^record/del/$', views.delete, name='record_del'),
    url(r'^record/save/$', views.message, name='record_message'),
    url(r'^record/edit/(?P<ids>\d+)/$', views.edit, name='record_edit'),
    url(r'^record/detail/(?P<ids>\d+)/$', views.detail, name='record_detail'),

    url(r'^record_list/$', record_list.record_list, name='record_list'),
    url(r'^record_list/delete/(?P<ids>\d+)/$', record_list.record_list_delete, name='record_list_delete'),
    url(r'^edit/(?P<ids>\d+)/$', record_list.edit, name='edit'),
    url(r'^record_list/add/$', record_list.add, name='record_list_add'),
    url(r'^arecord_list/save/$', record_list.message, name='arecord_list_message'),
    url(r'^record_list/edit/(?P<ids>\d+)/$', record_list.edit, name='record_list_edit'),
    url(r'^record_list/detail/(?P<ids>\d+)/$', record_list.detail, name='record_list_detail'),

    url(r'^faq/$', faq.faq, name='faq'),
    url(r'^faq/delete/(?P<ids>\d+)/$', faq.faq_delete, name='faq_delete'),
    url(r'^edit/(?P<ids>\d+)/$', faq.edit, name='edit'),
    url(r'^faq/add/$', faq.add, name='faq_add'),
    url(r'^faq/save/$', faq.message, name='faq_message'),
    url(r'^faq/edit/(?P<ids>\d+)/$', faq.edit, name='faq_edit'),
    url(r'^faq/detail/(?P<ids>\d+)/$', faq.detail, name='faq_detail'),

    url(r'^faq_list/$', faq_list.faq_list, name='faq_list'),
    url(r'^faq_list/delete/(?P<ids>\d+)/$', faq_list.faq_list_delete, name='faq_list_delete'),
    url(r'^edit/(?P<ids>\d+)/$', faq_list.edit, name='edit'),
    url(r'^faq_list/add/$', faq_list.add, name='faq_list_add'),
    url(r'^faq_list/save/$', faq_list.message, name='faq_list_message'),
    url(r'^faq_list/edit/(?P<ids>\d+)/$', faq_list.edit, name='faq_list_edit'),
    url(r'^faq_list/detail/(?P<ids>\d+)/$', faq_list.detail, name='faq_list_detail'),

    url(r'^assessment/$', assessment.assessment, name='assessment'),
    url(r'^assessment/delete/(?P<ids>\d+)/$', assessment.assessment_delete, name='assessment_delete'),
    url(r'^edit/(?P<ids>\d+)/$', assessment.edit, name='edit'),
    url(r'^assessment/add/$', assessment.add, name='assessment_add'),
    url(r'^assessment/save/$', assessment.message, name='assessment_message'),
    url(r'^assessment/edit/(?P<ids>\d+)/$', assessment.edit, name='assessment_edit'),
    url(r'^assessment/detail/(?P<ids>\d+)/$', assessment.detail, name='assessment_detail'),

    url(r'^assessment_list/$', assessment_list.assessment_list, name='assessment_list'),
    url(r'^assessment_list/delete/(?P<ids>\d+)/$', assessment_list.assessment_list_delete, name='assessment_list_delete'),
    url(r'^edit/(?P<ids>\d+)/$', assessment_list.edit, name='edit'),
    url(r'^assessment_list/add/$', assessment_list.add, name='assessment_list_add'),
    url(r'^assessment_list/save/$', assessment_list.message, name='assessment_list_message'),
    url(r'^assessment_list/edit/(?P<ids>\d+)/$', assessment_list.edit, name='assessment_list_edit'),
    url(r'^assessment_list/detail/(?P<ids>\d+)/$', assessment_list.detail, name='assessment_list_detail'),

    url(r'^change/$', change.change, name='change'),
    url(r'^change/delete/(?P<ids>\d+)/$', change.change_delete, name='change_delete'),
    url(r'^change/add/$', change.add, name='change_add'),
    url(r'^change/save/$', change.message, name='change_message'),
    url(r'^change/edit/(?P<ids>\d+)/$', change.edit, name='change_edit'),
    url(r'^change/detail/(?P<ids>\d+)/$', change.detail, name='change_detail'),

url(r'^track/$', track.track, name='track'),
    url(r'^track/delete/(?P<ids>\d+)/$', track.track_delete, name='track_delete'),
    url(r'^edit/(?P<ids>\d+)/$', track.edit, name='edit'),
    url(r'^track/add/$', track.add, name='track_add'),
    url(r'^track/save/$', track.message, name='track_message'),
    url(r'^track/edit/(?P<ids>\d+)/$', track.edit, name='track_edit'),
    url(r'^track/detail/(?P<ids>\d+)/$', track.detail, name='track_detail'),

    url(r'^track_list/$', track_list.track_list, name='track_list'),
    url(r'^track_list/delete/(?P<ids>\d+)/$', track_list.track_list_delete, name='track_list_delete'),
    url(r'^edit/(?P<ids>\d+)/$', track_list.edit, name='edit'),
    url(r'^track_list/add/$', track_list.add, name='track_list_add'),
    url(r'^track_list/save/$', track_list.message, name='track_list_message'),
    url(r'^track_list/edit/(?P<ids>\d+)/$', track_list.edit, name='track_list_edit'),
    url(r'^track_list/detail/(?P<ids>\d+)/$', track_list.detail, name='track_list_detail'),

    url(r'^memo/$', memo.memo, name='memo'),
    url(r'^memo/delete/(?P<ids>\d+)/$', memo.memo_delete, name='memo_delete'),
    url(r'^memo/add/$', memo.add, name='memo_add'),
    url(r'^memo/save/$', memo.message, name='memo_message'),
    url(r'^memo/edit/(?P<ids>\d+)/$', memo.edit, name='memo_edit'),
    url(r'^memo/detail/(?P<ids>\d+)/$', memo.detail, name='memo_detail'),

]
