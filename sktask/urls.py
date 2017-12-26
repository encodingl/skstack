#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views, ansible, shell, history, job, extravars, inventories, task
from sktask import project



urlpatterns = [
    url(r'ansible/$', ansible.index, name='ansible'),
    url(r'^shell/$', shell.index, name='shell'),
    url(r'^scripts/exec/$', shell.exec_scripts, name='exec_scripts'),
    url(r'^playbook/$', ansible.playbook, name='playbook'),
    url(r'^ansible/command/$', ansible.ansible_command, name='acommand'),
    url(r'^host/sync/$', ansible.host_sync, name='host_sync'),
    
    url(r'^history/$', history.index, name='history'),
    url(r'^history/detail/(?P<ids>\d+)/$', history.detail, name='history_detail'),
       
    url(r'^project/del/$', project.project_del, name='project_del'),
    url(r'^project/manage/$', project.project_manage, name='project_manage'),
    url(r'^project/add/$', project.project_add, name='project_add'),
    url(r'^project/edit/(?P<ids>\d+)/$', project.project_edit, name='project_edit'),
    
    url(r'^task/$', task.index, name='task'),
    url(r'^task/playbook/$', task.playbook, name='task_playbook'),
    url(r'^task/playbookback/$', task.playbook_back, name='task_playbook_back'),
    url(r'^task/jobsearch/$', task.job_search, name='job_search'),
    url(r'^task/varsearch/$', task.extravars_search, name='extravars_search'),
    

    url(r'^job/$', job.job_index, name='job_index'),
    url(r'^job/del/$', job.job_del, name='job_del'),
    url(r'^job/add/$', job.job_add, name='job_add'),
    
    url(r'^job/edit/(?P<ids>\d+)/$', job.job_edit, name='job_edit'),
    url(r'^job/detail/(?P<ids>\d+)/$', job.job_detail, name='job_detail'),
    

# 
    url(r'^extravars/$', extravars.extravars_index, name='extravars_index'),
    url(r'^extravars/del/$', extravars.extravars_del, name='extravars_del'),
    url(r'^extravars/add/$', extravars.extravars_add, name='extravars_add'),
    url(r'^extravars/edit/(?P<ids>\d+)/$', extravars.extravars_edit, name='extravars_edit'),
    
    url(r'^inventories/$', inventories.index, name='inventories'),
    
]