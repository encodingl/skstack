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
from lib.lib_git import get_git_tag
from .forms import TaskCommit_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime
from gittle import Gittle
import redis
import time
import json
from lib.lib_config import get_redis_config
from lib.lib_skdeploy import adv_task_step

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
    

    repo = Gittle(obj_path, origin_uri=obj_git_url)
    
    repo.pull
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


@login_required()
@permission_verify()
def TaskCommit_check(request):
    obj_env=request.POST.get('env') 
    obj_project = request.POST.get('project')  
    obj_git_commit = request.POST.get('commit_id')
    redis_chanel = obj_project + obj_env
    redis_chanel_message = redis_chanel+"message"
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
    
    result_pre_deploy = adv_task_step(hosts="localhost", env=obj_env, project=obj_project, task_file="pre_deploy.sh")
    conn.set(redis_chanel_message,result_pre_deploy) 
    if result_pre_deploy == "success":     
        conn.set(redis_chanel,"30") 
    else:
        conn.set(redis_chanel,"10")
        ret=conn.get(redis_chanel_message)
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json) 
          
    obj_path = git_path + obj_env + "/" + obj_project  
     
     
    result_post_deploy = adv_task_step(hosts="localhost", env=obj_env, project=obj_project, task_file="post_deploy.sh")   
    conn.set(redis_chanel_message,result_post_deploy) 
    if result_post_deploy == "success":     
        conn.set(redis_chanel,"100") 
    else:
        conn.set(redis_chanel,"70")
        ret=conn.get(redis_chanel_message)
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)  

   

@login_required()
@permission_verify()
def TaskCommit_checkstatus(request):
    obj_env=request.POST.get('env') 
    obj_project = request.POST.get('project')  
    redis_chanel=obj_project+obj_env
    conn = redis.Redis(host='127.0.0.1',password='redis0619')
    ret=conn.get(redis_chanel) 
    print "ret status :%s" % ret 
    obj_json = json.dumps(ret)
    return  HttpResponse(obj_json)   


    