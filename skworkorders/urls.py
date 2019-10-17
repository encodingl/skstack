#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from skworkorders import WorkOrderFlow, Environment, WorkOrder, WorkOrderGroup,WorkOrderCommit,Vars,VarsGroup,test_websocket,ConfigCenter

urlpatterns = [
      
     url(r'^WorkOrder/del/$', WorkOrder.WorkOrder_del, name='WorkOrder_del'),
     url(r'^WorkOrder/$', WorkOrder.WorkOrder_index, name='WorkOrder_index'),
     url(r'^WorkOrder/add/$', WorkOrder.WorkOrder_add, name='WorkOrder_add'),
     url(r'^WorkOrder/edit/$', WorkOrder.WorkOrder_edit, name='WorkOrder_edit'),
     url(r'^WorkOrder/off/$', WorkOrder.WorkOrder_off, name='WorkOrder_off'),
     url(r'^WorkOrder/on/$', WorkOrder.WorkOrder_on, name='WorkOrder_on'),
   
     url(r'^WorkOrder/template/$', WorkOrder.WorkOrder_template, name='WorkOrder_template'),
     url(r'^WorkOrder/add2/(?P<ids>\d+)/$', WorkOrder.WorkOrder_add_from_template, name='WorkOrder_add_from_template'),
     
     url(r'^WorkOrderGroup/$', WorkOrderGroup.WorkOrderGroup_index, name='WorkOrderGroup_index'),
     url(r'^WorkOrderGroup/del/$', WorkOrderGroup.WorkOrderGroup_del, name='WorkOrderGroup_del'),
     url(r'^WorkOrderGroup/add/$', WorkOrderGroup.WorkOrderGroup_add, name='WorkOrderGroup_add'),
     url(r'^WorkOrderGroup/edit/(?P<ids>\d+)/$', WorkOrderGroup.WorkOrderGroup_edit, name='WorkOrderGroup_edit'),
     
     url(r'^Environment/$', Environment.Environment_index, name='Environment_index'),
     url(r'^Environment/del/$', Environment.Environment_del, name='Environment_del'),
     url(r'^Environment/add/$', Environment.Environment_add, name='Environment_add'),
     url(r'^Environment/edit/(?P<ids>\d+)/$', Environment.Environment_edit, name='Environment_edit'),
     
     url(r'^ConfigCenter/$', ConfigCenter.ConfigCenter_index, name='ConfigCenter_index'),
     url(r'^ConfigCenter/del/$', ConfigCenter.ConfigCenter_del, name='ConfigCenter_del'),
     url(r'^ConfigCenter/add/$', ConfigCenter.ConfigCenter_add, name='ConfigCenter_add'),
     url(r'^ConfigCenter/edit/(?P<ids>\d+)/$', ConfigCenter.ConfigCenter_edit, name='ConfigCenter_edit'),
     url(r'^ConfigCenter/check/(?P<ids>\d+)/$', ConfigCenter.ConfigCenter_check, name='ConfigCenter_check'),
     

     
     url(r'^VarsGroup/$', VarsGroup.VarsGroup_index, name='VarsGroup_index'),
     url(r'^VarsGroup/del/$', VarsGroup.VarsGroup_del, name='VarsGroup_del'),
     url(r'^VarsGroup/add/$', VarsGroup.VarsGroup_add, name='VarsGroup_add'),
     url(r'^VarsGroup/edit/(?P<ids>\d+)/$', VarsGroup.VarsGroup_edit, name='VarsGroup_edit'),
     url(r'^VarsGroup/copy/$', VarsGroup.VarsGroup_copy, name='VarsGroup_copy'),

     url(r'^Vars/$', Vars.Vars_index, name='Vars_index'),
     url(r'^Vars/del/$', Vars.Vars_del, name='Vars_del'),
     url(r'^Vars/add/$', Vars.Vars_add, name='Vars_add'),
     url(r'^Vars/edit/(?P<ids>\d+)/$', Vars.Vars_edit, name='Vars_edit'),
     url(r'^Vars/check/(?P<ids>\d+)/$', Vars.Vars_check, name='Vars_check'),
     url(r'^Vars/copy/$', Vars.Vars_copy, name='Vars_copy'),
     
     
     url(r'^WorkOrderCommit/$', WorkOrderCommit.WorkOrderCommit_index, name='WorkOrderCommit_index'),
     url(r'^WorkOrderCommit/undo/$', WorkOrderCommit.WorkOrderCommit_undo, name='WorkOrderCommit_undo'),
     url(r'^WorkOrderCommit/add/(?P<ids>\d+)/$', WorkOrderCommit.WorkOrderCommit_add, name='WorkOrderCommit_add'),
     url(r'^WorkOrderCommit/help/(?P<ids>\d+)/$', WorkOrderCommit.WorkOrderCommit_help, name='WorkOrderCommit_help'),
     url(r'^WorkOrderCommit/pretask/$', WorkOrderCommit.pretask, name='WorkOrderCommit_pretask'),
         
     url(r'^WorkOrderFlow/audit/$', WorkOrderFlow.WorkOrderFlow_audit, name='WorkOrderFlow_audit'),
     url(r'^WorkOrderFlow/audit/permit/$', WorkOrderFlow.WorkOrderFlow_permit, name='WorkOrderFlow_permit'),
     url(r'^WorkOrderFlow/audit/deny/$', WorkOrderFlow.WorkOrderFlow_deny, name='WorkOrderFlow_deny'),  
     
     url(r'^WorkOrderFlow/release/foreground/$', WorkOrderFlow.WorkOrderFlow_foreground_release, name='WorkOrderFlow_foreground_release'),
     url(r'^WorkOrderFlow/release/backgroud/$', WorkOrderFlow.WorkOrderFlow_background_release, name='WorkOrderFlow_background_release'),
     url(r'^WorkOrderFlow/release/(?P<ids>\d+)/$', WorkOrderFlow.WorkOrderFlow_release, name='WorkOrderFlow_release'),
     url(r'^WorkOrderFlow/release/run/$', WorkOrderFlow.WorkOrderFlow_release_run, name='WorkOrderFlow_release_run'),
     url(r'^WorkOrderFlow/release/revoke/$', WorkOrderFlow.WorkOrderFlow_revoke, name='WorkOrderFlow_revoke'),
     
     url(r'^WorkOrderFlow/history/foreground/$', WorkOrderFlow.WorkOrderFlow_foreground_history, name='WorkOrderFlow_foreground_history'),
     url(r'^WorkOrderFlow/history/background/$', WorkOrderFlow.WorkOrderFlow_background_history, name='WorkOrderFlow_background_history'),
     url(r'^WorkOrderFlow/history/detail/background/$', WorkOrderFlow.WorkOrderFlow_background_detail, name='WorkOrderFlow_background_detail'),
     url(r'^WorkOrderFlow/history/detail/foreground/(?P<ids>\d+)/$', WorkOrderFlow.WorkOrderFlow_foreground_detail, name='WorkOrderFlow_foreground_detail'),
     
     
#      url(r'^websocket/$', test_websocket.websocket_index, name='websocket_index'),
#      url(r'^echo/$', test_websocket.echo, name='websocket_echo'),
 
    
]