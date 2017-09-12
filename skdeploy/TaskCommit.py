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
from git  import Git
from skaccounts.models import UserInfo,UserGroup,AuditFlow

level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)
git_path = get_dir("git_path")


@login_required()
@permission_verify()
def TaskCommit_index(request):
    temp_name = "skdeploy/skdeploy-header.html"    
 
    obj_user = UserInfo.objects.get(username=request.user)
    
    obj_group = obj_user.usergroup_set.all()
    obj_project = Project.objects.filter(user_dep__in=obj_group,status="yes")
    tpl_all = obj_project
   
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
    obj_title = str(obj_project) + "-" + str(obj_env)
    obj_audit = obj.audit_flow
    if not obj_audit:
        obj_level = "0" 
    else:
        obj_level = AuditFlow.objects.get(name=obj_audit).level
    

    repo = Gittle(obj_path, origin_uri=obj_git_url)
    
    repo.pull
    dic_init={'title':obj_title,
              'project':obj_project,
              'project_id':obj_project_id,
             'project_group':obj_project_group,
             'env':obj_env,
             'user_commit':obj_user,
             'branch':obj_branch,
             'status':"0",
             'audit_level':obj_level,
               
             
             }
    
    if request.method == 'POST':
        tpl_TaskCommit_form = TaskCommit_form(request.POST)
        if tpl_TaskCommit_form.is_valid():
            tpl_TaskCommit_form.save()
            status = 1
        else:
            status = 3
            list_tumple_tags=get_git_tag(obj_path,obj_git_url)     
            tpl_TaskCommit_form.fields["commit_id"].widget.choices=list_tumple_tags
    else:  
        tpl_TaskCommit_form = TaskCommit_form(initial=dic_init)  
        list_tumple_tags=get_git_tag(obj_path,obj_git_url)   
        tpl_TaskCommit_form.fields["commit_id"].widget.choices=list_tumple_tags
        list_tumple_hosts = [("127.0.0.1","127.0.0.1"),("127.0.0.2","127.0.0.2")]
        tpl_TaskCommit_form.fields["hosts_cus"].widget.choices = list_tumple_hosts
        
    
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
    
    if result_pre_deploy == "success": 
        result_pre_deploy = "pre_deploy task %s" % result_pre_deploy
        conn.set(redis_chanel_message,result_pre_deploy)     
        conn.set(redis_chanel,"30") 
    else:
        conn.set(redis_chanel,"5")
        ret=conn.get(redis_chanel_message)
        result_pre_deploy = "pre_deploy task %s" % result_pre_deploy
        conn.set(redis_chanel_message,result_pre_deploy) 
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json) 
    
    result_pre_deploy=conn.get(redis_chanel_message)
    
         
    obj_path = git_path + obj_env + "/" + obj_project  
    g = Git(obj_path)  
    g.checkout(obj_git_commit)
    conn.set(redis_chanel,"60")
    conn.set(redis_chanel_message,"git checkout success")
    
    result_git_task=conn.get(redis_chanel_message)

     
     
    result_post_deploy = adv_task_step(hosts="localhost", env=obj_env, project=obj_project, task_file="post_deploy.sh")        
    if result_post_deploy == "success":     
        conn.set(redis_chanel,"100") 
        result_post_deploy = "post_deploy task %s" % result_post_deploy
        conn.set(redis_chanel_message,result_post_deploy) 
        ret="ok"
        obj_json = json.dumps(ret)
        result_post_deploy=conn.get(redis_chanel_message)
       
        return  HttpResponse(obj_json) 
    else:
        conn.set(redis_chanel,"65")
        ret=conn.get(redis_chanel_message)
        result_post_deploy = "post_deploy task %s" % result_post_deploy
        conn.set(redis_chanel_message,result_post_deploy)
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)  
    
    
    
   

@login_required()
@permission_verify()
def TaskCommit_checkstatus(request):
    obj_env=request.POST.get('env') 
    obj_project = request.POST.get('project')  
    redis_chanel=obj_project+obj_env
    redis_chanel_message = redis_chanel+"message"
    ret={}
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
    ret["redis_chanel"]=conn.get(redis_chanel) 
    ret["redis_chanel_message"]=conn.get(redis_chanel_message)
    if "faild" in ret["redis_chanel_message"] or ret["redis_chanel"] == "100" :
        conn.delete(redis_chanel)
        print conn.get(redis_chanel)
        conn.delete(redis_chanel_message)
    
    obj_json = json.dumps(ret)
    return  HttpResponse(obj_json)   


    