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
         
     url(r'^TaskStatus/$', TaskStatus.TaskStatus_index, name='TaskStatus_index'),
     url(r'^TaskStatus/del/$', TaskStatus.TaskStatus_del, name='TaskStatus_del'),
     url(r'^TaskStatus/add/$', TaskStatus.TaskStatus_add, name='TaskStatus_add'),
     url(r'^TaskStatus/edit/(?P<ids>\d+)/$', TaskStatus.TaskStatus_edit, name='TaskStatus_edit'),
     
     url(r'^TaskCommit/$', TaskCommit.TaskCommit_index, name='TaskCommit_index'),
     url(r'^TaskCommit/undo/$', TaskCommit.TaskCommit_undo, name='TaskCommit_undo'),
     url(r'^TaskCommit/add/(?P<ids>\d+)/$', TaskCommit.TaskCommit_add, name='TaskCommit_add'),
 
    
]