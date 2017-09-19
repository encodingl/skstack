#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from skcmdb import api, idc, asset, ops

urlpatterns = [
    url(r'asset/$', asset.asset, name='cmdb'),
    url(r'^asset/add/$', asset.asset_add, name='asset_add'),
    url(r'^asset/del/$', asset.asset_del, name='asset_del'),
    url(r'^asset/asset_import/$', asset.asset_import, name='asset_import'),
    url(r'^asset/edit/(?P<ids>\d+)/$', asset.asset_edit, name='asset_edit'),
    url(r'asset/app_list$', ops.app_list, name='app_list'),
    url(r'^asset/app_add/$', ops.app_add, name='app_add'),
    url(r'^asset/app_del/$', ops.app_del, name='app_del'),
    url(r'^asset/app_edit/(?P<ids>\d+)/$', ops.app_edit, name='app_edit'),
    url(r'asset/url_list$', ops.url_list, name='url_list'),
    url(r'asset/url_add$', ops.url_add, name='url_add'),
    url(r'asset/url_del$', ops.url_del, name='url_del'),
    url(r'asset/url_edit/(?P<ids>\d+)$', ops.url_edit, name='url_edit'),
    url(r'asset/kafka_list$', ops.kafka_list, name='kafka_list'),
    url(r'asset/kafka_update$', ops.kafka_update, name='kafka_update'),
    url(r'asset/opssa_list/$', ops.opssa_list, name='opssa_list'),
    url(r'asset/env_list/$', ops.env_list, name='env_list'),
    url(r'asset/env_add/$', ops.env_add, name='env_add'),
    url(r'asset/env_del/$', ops.env_del, name='env_del'),
    url(r'^asset/env_edit/(?P<ids>\d+)/$', ops.env_edit, name='env_edit'),
    url(r'asset/ywgroup_list/$', ops.ywgroup_list, name='ywgroup_list'),
    url(r'asset/ywgroup_add/$', ops.ywgroup_add, name='ywgroup_add'),
    url(r'asset/ywgroup_del/$', ops.ywgroup_del, name='ywgroup_del'),
    url(r'^asset/ywgroup_edit/(?P<ids>\d+)/$', ops.ywgroup_edit, name='ywgroup_edit'),
    url(r'asset/ywgroup_save$', ops.ywgroup_save, name='ywgroup_save'),
    url(r'asset/hostgroup_list/$', ops.hostgroup_list, name='hostgroup_list'),
    url(r'asset/hostgroup_add/$', ops.hostgroup_add, name='hostgroup_add'),
    url(r'asset/hostgroup_del/$', ops.hostgroup_del, name='hostgroup_del'),
    url(r'^asset/hostgroup_edit/(?P<ids>\d+)/$', ops.hostgroup_edit, name='hostgroup_edit'),
    url(r'asset/hostgroup_save$', ops.hostgroup_save, name='hostgroup_save'),
    url(r'asset/middletype_list/$', ops.middletype_list, name='middletype_list'),
    url(r'asset/middletype_add/$', ops.middletype_add, name='middletype_add'),
    url(r'asset/middletype_del/$', ops.middletype_del, name='middletype_del'),
    url(r'^asset/middletype_edit/(?P<ids>\d+)/$', ops.middletype_edit, name='middletype_edit'),
    url(r'asset/middletype_save$', ops.middletype_save, name='middletype_save'),
    url(r'asset/dbsource_list$', ops.dbsource_list, name='dbsource_list'),
    url(r'asset/dbsource_add$', ops.dbsource_add, name='dbsource_add'),
    url(r'asset/dbsource_del$', ops.dbsource_del, name='dbsource_del'),
    url(r'asset/dbsource_edit/(?P<ids>\d+)$', ops.dbsource_edit, name='dbsource_edit'),
    url(r'^idc/$', idc.idc, name='idc'),
    url(r'^idc/add/$', idc.idc_add, name='idc_add'),
    url(r'^idc/del/$', idc.idc_del, name='idc_del'),
    url(r'^idc/save/$', idc.idc_save, name='idc_save'),
    url(r'^idc/edit/(?P<ids>\d+)/$', idc.idc_edit, name='idc_edit'),
    url(r'^collect', api.collect, name='update_api'),
    url(r'^get/host/', api.get_host, name='get_host'),
    url(r'^get/group/', api.get_group, name='get_group'),
]
