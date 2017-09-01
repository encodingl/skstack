#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,TaskStatus,ProjectGroup,Project,TaskStatus
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log
from .forms import TaskStatus_detail_form,TaskStatus_release_form,TaskStatus_rollback_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime
from lib.lib_skdeploy import adv_task_step, release_project,change_link
import redis
from lib.lib_config import get_redis_config
from lib.file import get_ex_link

import time



@login_required()
@permission_verify()
def TaskStatus_index(request):
    temp_name = "skdeploy/skdeploy-header.html"    
    tpl_all = TaskStatus.objects.all()
    
    return render_to_response('skdeploy/TaskStatus_index.html', locals(), RequestContext(request))





@login_required()
@permission_verify()
def TaskStatus_del(request):
#    temp_name = "skdeploy/skdeploy-header.html"
    TaskStatus_id = request.GET.get('id', '')
    if TaskStatus_id:
        TaskStatus.objects.filter(id=TaskStatus_id).delete()
    
    if request.method == 'POST':
        TaskStatus_items = request.POST.getlist('x_check', [])
        if TaskStatus_items:
            for n in TaskStatus_items:
                TaskStatus.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allproject = TaskStatus.objects.all()
    
 #   return render_to_response("skdeploy/TaskStatus.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def TaskStatus_detail(request, ids):
    
    obj = get_object(TaskStatus, id=ids)
    tpl_TaskStatus_form = TaskStatus_detail_form(instance=obj)      
    return render_to_response("skdeploy/TaskStatus_detail.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def TaskStatus_release(request, ids):
    temp_name = "skdeploy/skdeploy-header.html"
    obj = get_object(TaskStatus, id=ids) 
    obj_title=obj.title
    if obj_title.endswith('-rollback'):
        dic_init={'project':obj.project,
              'project_id':obj.project_id,          
             'env':obj.env,
             'desc':obj.desc,
         
             }
        tpl_TaskStatus_release_form = TaskStatus_rollback_form(initial=dic_init)  
        return render_to_response("skdeploy/TaskStatus_rollback.html", locals(), RequestContext(request))
    
    else:
        dic_init={'project':obj.project,
                  'project_id':obj.project_id,          
                 'env':obj.env,
                 'commit_id':obj.commit_id,             
                 }
        tpl_TaskStatus_release_form = TaskStatus_release_form(initial=dic_init)  
        return render_to_response("skdeploy/TaskStatus_release.html", locals(), RequestContext(request))



 
    
    

@login_required()
@permission_verify()
def TaskStatus_release_run(request):
#     temp_name = "skdeploy/skdeploy-header.html"
    TaskStatus_id = request.POST.get('id')
  
    if TaskStatus_id:
        obj = TaskStatus.objects.get(id=TaskStatus_id)
    obj_project = obj.project

    obj_env = obj.env
    obj_project_id = obj.project_id
    
    
    obj2 = Project.objects.get(id=obj_project_id)
    obj_hosts = obj2.hosts 
    now_time = time.strftime("%Y%m%d-%H%M%S")
 
    if obj2.release_library.endswith('/'):
   
        obj_release_dir = obj2.release_library + obj_project + "/" + now_time + "/" 
    else:
        obj_release_dir = obj2.release_library + "/" + obj_project + "/" + now_time
    obj_release_to = obj2.release_to
    obj_ex_link_id = get_ex_link(hosts=obj_hosts,dir=obj2.release_to)
    redis_chanel = obj_project + obj_env
    redis_chanel_message = redis_chanel+"message"
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
     
    result_release_project = release_project(project=obj_project,env=obj_env,hosts=obj_hosts,release_dir=obj_release_dir,release_to=obj_release_to)
    if result_release_project == "success": 
        result_release_project = "file sync task %s" % result_release_project
        conn.set(redis_chanel_message,result_release_project)     
        conn.set(redis_chanel,"25") 
    else:
        conn.set(redis_chanel,"5")
        ret=conn.get(redis_chanel_message)
        result_release_project = "file sync  task %s" % result_release_project
        conn.set(redis_chanel_message,result_release_project) 
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)    
  
 
    
    
    result_pre_release = adv_task_step(hosts=obj_hosts, env=obj_env, project=obj_project, task_file="pre_release.sh")
    if result_pre_release == "success": 
        result_pre_release = "pre_release task %s" % result_pre_release
        conn.set(redis_chanel_message,result_pre_release)     
        conn.set(redis_chanel,"50") 
        result_pre_release=conn.get(redis_chanel_message)
       
    else:
        conn.set(redis_chanel,"30")
        ret=conn.get(redis_chanel_message)
        result_pre_release = "pre_release task %s" % result_pre_release
        conn.set(redis_chanel_message,result_pre_release) 
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)    
    
    result_change_link = change_link(hosts=obj_hosts,release_dir=obj_release_dir,release_to=obj_release_to)
    if result_change_link == "success": 
        result_change_link = "change soft link task %s" % result_change_link
        conn.set(redis_chanel_message,result_change_link)     
        conn.set(redis_chanel,"75") 
    else:
        conn.set(redis_chanel,"55")
        ret=conn.get(redis_chanel_message)
        result_change_link = "change soft link task %s" % result_change_link
        conn.set(redis_chanel_message,result_change_link) 
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json) 
    
    result_post_release = adv_task_step(hosts=obj_hosts, env=obj_env, project=obj_project, task_file="post_release.sh")
    if result_post_release == "success": 
        result_post_release = "post_release task %s" % result_post_release
        conn.set(redis_chanel_message,result_post_release)     
        conn.set(redis_chanel,"100") 
        ret="ok"
        obj_json = json.dumps(ret)
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TaskStatus.objects.filter(id=TaskStatus_id).update(status="3",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at)
        result_post_release=conn.get(redis_chanel_message)
    
        
        return  HttpResponse(obj_json)
    else:
        conn.set(redis_chanel,"80")
        ret=conn.get(redis_chanel_message)
        result_post_release = "post_release task %s" % result_post_release
        conn.set(redis_chanel_message,result_post_release) 
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)    
    
 
    



@login_required()
@permission_verify()
def TaskStatus_release_status(request):
    TaskStatus_id = request.POST.get('id') 
    obj = TaskStatus.objects.get(id=TaskStatus_id)
    obj_project = obj.project
    obj_env = obj.env 
    redis_chanel=obj_project+obj_env
    
    redis_chanel_message = redis_chanel+"message"
    ret={}
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
    ret["redis_chanel"]=conn.get(redis_chanel) 

    ret["redis_chanel_message"]=conn.get(redis_chanel_message)
    
    obj_json = json.dumps(ret)
    if (ret["redis_chanel_message"] is not None and "faild" in ret["redis_chanel_message"]) or (ret["redis_chanel"] is not None and ret["redis_chanel"])  == "100" :
        conn.delete(redis_chanel)
       
        conn.delete(redis_chanel_message)
    return  HttpResponse(obj_json) 


@login_required()
@permission_verify()
def TaskStatus_rollback_add(request, ids):
    temp_name = "skdeploy/skdeploy-header.html"
    obj = get_object(TaskStatus, id=ids) 
    obj_title = str(obj.project) + "-" + str(obj.env) + "-" + "rollback"
    obj_status = 3
    obj_desc = "The original task id " + str(obj.id) + " rollback:" + "\nfrom: " + str(obj.link_id) + "\nto: " + str(obj.ex_link_id)
    dic_rollback={
             'title':obj_title,
             'project':obj.project,
             'project_id':obj.project_id,          
             'env':obj.env,
             'link_id':obj.ex_link_id,
             'commit_id':obj.commit_id,
             'project_group':obj.project_group,
             'branch':obj.branch,
             'desc':obj_desc,
             'status':"0",
             'user_commit':request.user,
             
             }

    TaskStatus.objects.create(**dic_rollback)
    tpl_all = TaskStatus.objects.all()
    return render_to_response("skdeploy/TaskStatus_index.html", locals(), RequestContext(request))




    
@login_required()
@permission_verify()
def TaskStatus_rollback_run(request):
#     temp_name = "skdeploy/skdeploy-header.html"
    TaskStatus_id = request.POST.get('id') 
    if TaskStatus_id:
        obj = TaskStatus.objects.get(id=TaskStatus_id)
    obj_project = obj.project
    obj_env = obj.env
    obj_project_id = obj.project_id
    obj2 = Project.objects.get(id=obj_project_id)
    redis_chanel = obj_project + obj_env
    redis_chanel_message = redis_chanel+"message"
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)  
    result_change_link = change_link(hosts=obj2.hosts ,release_dir=obj.link_id,release_to=obj2.release_to )
    if result_change_link == "success": 
        result_change_link = "change soft link task %s" % result_change_link
        conn.set(redis_chanel_message,result_change_link)     
        conn.set(redis_chanel,"50") 
    else:
        conn.set(redis_chanel,"5")
        ret=conn.get(redis_chanel_message)
        result_change_link = "change soft link task %s" % result_change_link
        conn.set(redis_chanel_message,result_change_link) 
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json) 
    
    result_post_release = adv_task_step(hosts=obj2.hosts , env=obj_env, project=obj_project, task_file="post_release.sh")
    if result_post_release == "success": 
        result_post_release = "post_release task %s" % result_post_release
        conn.set(redis_chanel_message,result_post_release)     
        conn.set(redis_chanel,"100") 
        ret="ok"
        obj_json = json.dumps(ret)
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TaskStatus.objects.filter(id=TaskStatus_id).update(status="3",finished_at=obj_finished_at)
        result_post_release=conn.get(redis_chanel_message)
        return  HttpResponse(obj_json)
    else:
        conn.set(redis_chanel,"55")
        ret=conn.get(redis_chanel_message)
        result_post_release = "post_release task %s" % result_post_release
        conn.set(redis_chanel_message,result_post_release) 
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)    
    