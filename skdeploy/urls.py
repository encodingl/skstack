#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from skdeploy import TaskStatus, Environment, Project, ProjectGroup,TaskCommit

urlpatterns = [
      
     url(r'^Project/del/$', Project.Project_del, name='Project_del'),
     url(r'^Project/$', Project.Project_index, name='Project_index'),
     url(r'^Project/add/$', Project.Project_add, name='Project_add'),
     url(r'^Project/edit/(?P<ids>\d+)/$', Project.Project_edit, name='Project_edit'),
     
     url(r'^ProjectGroup/$', ProjectGroup.ProjectGroup_index, name='ProjectGroup_index'),
     url(r'^ProjectGroup/del/$', ProjectGroup.ProjectGroup_del, name='ProjectGroup_del'),
     url(r'^ProjectGroup/add/$', ProjectGroup.ProjectGroup_add, name='ProjectGroup_add'),
     url(r'^ProjectGroup/edit/(?P<ids>\d+)/$', ProjectGroup.ProjectGroup_edit, name='ProjectGroup_edit'),
     
     url(r'^Environment/$', Environment.Environment_index, name='Environment_index'),
     url(r'^Environment/del/$', Environment.Environment_del, name='Environment_del'),
     url(r'^Environment/add/$', Environment.Environment_add, name='Environment_add'),
     url(r'^Environment/edit/(?P<ids>\d+)/$', Environment.Environment_edit, name='Environment_edit'),
         
     
     url(r'^TaskStatus/revoke/$', TaskStatus.TaskStatus_revoke, name='TaskStatus_revoke'),
     url(r'^TaskStatus/release/(?P<ids>\d+)/$', TaskStatus.TaskStatus_release, name='TaskStatus_release'),
     url(r'^TaskStatus/release/run/$', TaskStatus.TaskStatus_release_run, name='TaskStatus_release_run'),
     url(r'^TaskStatus/release/status/$', TaskStatus.TaskStatus_release_status, name='TaskStatus_release_status'),
     
     url(r'^TaskStatus/rollback/run/$', TaskStatus.TaskStatus_rollback_run, name='TaskStatus_rollback_run'),
#      url(r'^TaskStatus/rollback/add/(?P<ids>\d+)/$', TaskStatus.TaskStatus_rollback_add, name='TaskStatus_rollback_add'),
     url(r'^TaskStatus/rollback/add/$', TaskStatus.TaskStatus_rollback_add, name='TaskStatus_rollback_add'),
    
     url(r'^TaskStatus/detail/(?P<ids>\d+)/$', TaskStatus.TaskStatus_detail, name='TaskStatus_detail'),
     url(r'^TaskStatus/$', TaskStatus.TaskStatus_index, name='TaskStatus_index'),
     url(r'^TaskStatus/history/$', TaskStatus.TaskStatus_history, name='TaskStatus_history'),
     url(r'^TaskStatus/audit/$', TaskStatus.TaskStatus_audit, name='TaskStatus_audit'),
     url(r'^TaskStatus/audit/permit/$', TaskStatus.TaskStatus_permit, name='TaskStatus_permit'),
     url(r'^TaskStatus/audit/deny/$', TaskStatus.TaskStatus_deny, name='TaskStatus_deny'),
  
     
     url(r'^TaskStatus/TaskCommit/$', TaskCommit.TaskCommit_index, name='TaskCommit_index'),
     url(r'^TaskCommit/undo/$', TaskCommit.TaskCommit_undo, name='TaskCommit_undo'),
     url(r'^TaskCommit/add/(?P<ids>\d+)/$', TaskCommit.TaskCommit_add, name='TaskCommit_add'),
     url(r'^TaskCommit/check/$', TaskCommit.TaskCommit_check, name='TaskCommit_check'),
     url(r'^TaskCommit/checkstatus/$', TaskCommit.TaskCommit_checkstatus, name='TaskCommit_checkstatus'),
 
    
]