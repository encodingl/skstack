#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from skaccounts import user, role, permission, AuditFlow, UserGroup

urlpatterns = [
    url(r'^login/$', user.login, name='login'),
    url(r'^logout/$', user.logout, name='logout'),
    url(r'^user/list/$', user.user_list, name='user_list'),
    url(r'^user/add/$', user.user_add, name='user_add'),
    url(r'^user/delete/$', user.user_del, name='user_del'),
    url(r'^user/edit/(?P<ids>\d+)/$', user.user_edit, name='user_edit'),
    url(r'^reset/password/(?P<ids>\d+)/$', user.reset_password, name='reset_password'),
    url(r'^change/password/$', user.change_password, name='change_password'),
    url(r'^role/add/$', role.role_add, name='role_add'),
    url(r'^role/list/$', role.role_list, name='role_list'),
    url(r'^role/edit/(?P<ids>\d+)/$', role.role_edit, name='role_edit'),
    url(r'^role/delete/(?P<ids>\d+)/$', role.role_del, name='role_del'),

    url(r'^rolejob/add/$', role.role_job_add, name='role_job_add'),
    url(r'^rolejob/list/$', role.role_job_list, name='role_job_list'),
    url(r'^rolejob/edit/(?P<ids>\d+)/$', role.role_job_edit, name='role_job_edit'),
    url(r'^rolejob/delete/(?P<ids>\d+)/$', role.role_job_del, name='role_job_del'),
    url(r'^permission/deny/$', permission.permission_deny, name='permission_deny'),
    url(r'^permission/add/$', permission.permission_add, name='permission_add'),
    url(r'^permission/list/$', permission.permission_list, name='permission_list'),
    url(r'^permission/edit/(?P<ids>\d+)/$', permission.permission_edit, name='permission_edit'),
    url(r'^permission/delete/(?P<ids>\d+)/$', permission.permission_del, name='permission_del'),

    url(r'^UserGroup/$', UserGroup.UserGroup_index, name='UserGroup_index'),
    url(r'^UserGroup/del/$', UserGroup.UserGroup_del, name='UserGroup_del'),
    url(r'^UserGroup/add/$', UserGroup.UserGroup_add, name='UserGroup_add'),
    url(r'^UserGroup/edit/(?P<ids>\d+)/$', UserGroup.UserGroup_edit, name='UserGroup_edit'),

    url(r'^AuditFlow/$', AuditFlow.AuditFlow_index, name='AuditFlow_index'),
    url(r'^AuditFlow/del/$', AuditFlow.AuditFlow_del, name='AuditFlow_del'),
    url(r'^AuditFlow/add/$', AuditFlow.AuditFlow_add, name='AuditFlow_add'),
    url(r'^AuditFlow/edit/(?P<ids>\d+)/$', AuditFlow.AuditFlow_edit, name='AuditFlow_edit'),

    #     url(r'^AuditFlow/$', AuditFlow.AuditFlow_index, name='AuditFlow_index'),
    #     url(r'^AuditFlow/del/$', AuditFlow.AuditFlow_del, name='AuditFlow_del'),
    #     url(r'^AuditFlow/add/$', AuditFlow.AuditFlow_add, name='AuditFlow_add'),
    #     url(r'^AuditFlow/edit/(?P<ids>\d+)/$', AuditFlow.AuditFlow_edit, name='AuditFlow_edit'),
]
