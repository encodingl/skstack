#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,ProjectGroup,Project,TaskStatus,Environment
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log
from lib.git import get_git_tag
from .forms import TaskCommit_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime
from gittle import Gittle

level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)
git_path = get_dir("git_path")


@login_required()
@permission_verify()
def TaskCommit_index(request):
    temp_name = "skdeploy/skdeploy-header.html"    
    tpl_all = Project.objects.all()
    print tpl_all
    return render_to_response('skdeploy/TaskCommit_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def TaskCommit_undo(request):
#    temp_name = "skdeploy/skdeploy-header.html"
    TaskCommit_id = request.GET.get('id', '')
    if TaskCommit_id:
        TaskStatus.objects.filter(id=TaskCommit_id).delete()
    
    if request.method == 'POST':
        TaskCommit_items = request.POST.getlist('x_check', [])
        if TaskCommit_items:
            for n in TaskCommit_items:
                TaskStatus.objects.filter(id=n).delete()
    return HttpResponse(u'撤销成功')
 #   allproject = TaskCommit.objects.all()
    
 #   return render_to_response("skdeploy/TaskCommit.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def TaskCommit_add(request, ids):
    status = 0
    obj = get_object(Project, id=ids)
    obj_project_id = obj.id
    obj_project=obj.name
    obj_project_group=obj.group
    obj_env=obj.env
    obj_branch="master"
    obj_user=request.user    
    obj_path = git_path + str(obj_env) + "/" + str(obj_project)
    obj_git_url=obj.repo_url 
    
    print type(obj_pre_deploy)
#     repo = Gittle(obj_path, origin_uri=obj_git_url)
#     repo.pull()
    dic_init={'project':obj_project,
              'project_id':obj_project_id,
             'project_group':obj_project_group,
             'env':obj_env,
             'user_commit':obj_user,
             'branch':obj_branch,
             
             }
    
    if request.method == 'POST':
        tpl_TaskCommit_form = TaskCommit_form(request.POST, initial=dic_init)
        if tpl_TaskCommit_form.is_valid():
            tpl_TaskCommit_form.save()
            status = 1
        else:
            status = 2
    else:  
        tpl_TaskCommit_form = TaskCommit_form(initial=dic_init)  
        list_tumple_tags=get_git_tag(obj_path,obj_git_url)     
        tpl_TaskCommit_form.fields["commit_id"].widget.choices=list_tumple_tags
        
    
    
    return render_to_response("skdeploy/TaskCommit_add.html", locals(), RequestContext(request))





    