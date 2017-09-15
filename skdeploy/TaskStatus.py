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
from lib.lib_skdeploy import adv_task_step, release_project,change_link,uni_to_str
import redis
from lib.lib_config import get_redis_config
from lib.file import get_ex_link

import time
from skaccounts.models import UserInfo,UserGroup
from django.db.models import Q
from itertools import chain
from django.db.models import Max


@login_required()
@permission_verify()
def TaskStatus_index(request):
    temp_name = "skdeploy/skdeploy-header.html"    
    
    tpl_all = TaskStatus.objects.filter(user_commit=request.user)
#     obj_user = UserInfo.objects.get(username=request.user)    
#     obj_group = obj_user.usergroup_set.all()
#   
#     obj_AuditFlow = AuditFlow.objects.filter(Q(l1__in=obj_group)|Q(l2__in=obj_group)|Q(l3__in=obj_group))
#     obj_project = Project.objects.filter(audit_flow__in = obj_AuditFlow)
#     obj_project_audit = TaskStatus.objects.filter(project_id__in=obj_project)
# 
#     tpl_all = list(chain(obj_user_commit, obj_project_audit))
#     tpl_all = list(set(tpl_all))
   
    return render_to_response('skdeploy/TaskStatus_index.html', locals(), RequestContext(request))





@login_required()
@permission_verify()
def TaskStatus_revoke(request):
#     temp_name = "skdeploy/skdeploy-header.html"
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    TaskStatus_id = request.GET.get('id', '')
    if TaskStatus_id:
        TaskStatus.objects.filter(id=TaskStatus_id).update(status="9",finished_at=time_now)
    
    if request.method == 'POST':
        TaskStatus_items = request.POST.getlist('x_check', [])
        if TaskStatus_items:
            for n in TaskStatus_items:
                TaskStatus.objects.filter(id=n).update(status="9",finished_at=time_now)
    return HttpResponse(u'撤销成功')
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
                 'forks':obj.forks,            
                 }
        tpl_TaskStatus_release_form = TaskStatus_release_form(initial=dic_init)  
        return render_to_response("skdeploy/TaskStatus_release.html", locals(), RequestContext(request))



 
    
    

@login_required()
@permission_verify()
def TaskStatus_release_run(request):
    """release步骤发布视图函数
    主要分为如下几个部分：
    1 判断是否通过审核，只有通过审核后才能进行上线
    2 判断是否重复执行，一个环境中的一个项目只同时发布一次
    3 同步项目文件
    4 执行pre-release步骤脚本
    5 修改目标实例项目运行目录软链接
    6 执行post-release步骤脚本
    """
    TaskStatus_id = request.POST.get('id')
  
    if TaskStatus_id:
        obj = TaskStatus.objects.get(id=TaskStatus_id)
    obj_project = obj.project

    obj_env = obj.env
    obj_project_id = obj.project_id
    obj_status = obj.status
    obj_audit_level = obj.audit_level
    obj_forks = obj.forks
    
    
    
    obj2 = Project.objects.get(id=obj_project_id)
    if obj.hosts_cus:
        
        obj_hosts = uni_to_str(obj.hosts_cus)
    else:
        obj_hosts = obj2.hosts 
        
    print obj_hosts
    now_time = time.strftime("%Y%m%d-%H%M%S")
 
    if obj2.release_library.endswith('/'):
   
        obj_release_dir = obj2.release_library + obj_project + "/" + now_time + "/" 
    else:
        obj_release_dir = obj2.release_library + "/" + obj_project + "/" + now_time
    obj_release_to = obj2.release_to
#     obj_ex_link_id = get_ex_link(hosts=obj_hosts,dir=obj2.release_to)
    obj3 = TaskStatus.objects.filter(title=obj.title,status="3").aggregate(Max('link_id'))
    obj_ex_link_id = obj3["link_id__max"]
  
    redis_chanel = obj_project + obj_env
    redis_chanel_message = redis_chanel+"message"
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
    redis_chanel_pid_lock = redis_chanel + obj_project_id
#步骤1判断是否通过审核
    if (obj_audit_level == "1" and obj_status != "1") or (obj_audit_level == "2" and obj_status != "5") or (obj_audit_level == "3" and obj_status != "7") :
        conn.set(redis_chanel_message,"faild,Not yet permitted,any other problems, please contact the administrator")     
        conn.set(redis_chanel,"2")        
        ret=conn.get(redis_chanel_message)
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)
    else:
        pass
    #步骤2 判断是否重复执行   
    if conn.get(redis_chanel_pid_lock == "1") :
        conn.set(redis_chanel_message,"You have already submitted, or someone else is submitting the same project.ny other problems, please contact the administrator")     
        conn.set(redis_chanel,"2")        
        ret=conn.get(redis_chanel_message)
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)
        
    else:
        conn.set(redis_chanel_pid_lock,"1")

# 步骤3 同步project文件
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
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TaskStatus.objects.filter(id=TaskStatus_id).update(status="4",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at)
        obj_json = json.dumps(ret)
        conn.set(redis_chanel_pid_lock,"0")
        return  HttpResponse(obj_json)    
  
 
    
# 步骤4 执行pre release任务
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
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TaskStatus.objects.filter(id=TaskStatus_id).update(status="4",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at)
        obj_json = json.dumps(ret)
        conn.set(redis_chanel_pid_lock,"0")
        return  HttpResponse(obj_json)    
   
#步骤5 改变软链接
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
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TaskStatus.objects.filter(id=TaskStatus_id).update(status="4",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at) 
        obj_json = json.dumps(ret)
        conn.set(redis_chanel_pid_lock,"0")
        return  HttpResponse(obj_json) 
# 步骤6 执行post release任务
    result_post_release = adv_task_step(hosts=obj_hosts, env=obj_env, project=obj_project, task_file="post_release.sh",forks=obj_forks)
    if result_post_release == "success": 
        result_post_release = "post_release task %s" % result_post_release
        conn.set(redis_chanel_message,result_post_release)     
        conn.set(redis_chanel,"100") 
        ret="ok"
        obj_json = json.dumps(ret)
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TaskStatus.objects.filter(id=TaskStatus_id).update(status="3",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at)
        result_post_release=conn.get(redis_chanel_message)
    
        conn.set(redis_chanel_pid_lock,"0")
        return  HttpResponse(obj_json)
    else:
        conn.set(redis_chanel,"80")
        ret=conn.get(redis_chanel_message)
        result_post_release = "post_release task %s" % result_post_release
        conn.set(redis_chanel_message,result_post_release) 
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TaskStatus.objects.filter(id=TaskStatus_id).update(status="4",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at)
        obj_json = json.dumps(ret)
        conn.set(redis_chanel_pid_lock,"0")
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
def TaskStatus_rollback_add(request):
    temp_name = "skdeploy/skdeploy-header.html"
    TaskStatus_id = request.GET.get('id', '')
    obj = get_object(TaskStatus, id=TaskStatus_id) 
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
    
    
@login_required()
@permission_verify()
def TaskStatus_history(request):
    temp_name = "skdeploy/skdeploy-header.html"    
    
    tpl_all = TaskStatus.objects.all()
  
   
    return render_to_response('skdeploy/TaskStatus_history.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def TaskStatus_audit(request):
    temp_name = "skdeploy/skdeploy-header.html"    
    
#     obj_user_commit = TaskStatus.objects.filter(user_commit=request.user)
    obj_user = UserInfo.objects.get(username=request.user)    
    obj_group = obj_user.usergroup_set.all()
  
    obj_AuditFlow = AuditFlow.objects.filter(Q(l1__in=obj_group)|Q(l2__in=obj_group)|Q(l3__in=obj_group))
    obj_project = Project.objects.filter(audit_flow__in = obj_AuditFlow,audit_enable=True)
    tpl_all = TaskStatus.objects.filter(project_id__in=obj_project)

#     tpl_all = list(chain(obj_user_commit, obj_project_audit))
#     tpl_all = list(set(tpl_all))
   
    return render_to_response('skdeploy/TaskStatus_audit.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def TaskStatus_permit(request):
#     temp_name = "skdeploy/skdeploy-header.html"
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   
    TaskStatus_id = request.GET.get('id', '')
    login_user = request.user
  
    login_user = str(login_user)
   
    
    obj_user = UserInfo.objects.get(username=request.user)    
    obj_group = obj_user.usergroup_set.all()
    
    
    obj_TaskStatus = TaskStatus.objects.get(id=TaskStatus_id)
    obj_Project = Project.objects.get(id=obj_TaskStatus.project_id)

    obj_AuditFlow = AuditFlow.objects.get(name = obj_Project.audit_flow)
  
    
    obj_level = obj_AuditFlow.level
    if obj_level == "1":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        if obj_l1 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="1",user_l1=login_user,updated_at_l1=time_now)
            
    elif obj_level == "2":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)   
        if obj_l1 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="1",user_l1=login_user,updated_at_l1=time_now)
        if obj_l2 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="5",user_l2=login_user,updated_at_l2=time_now)
            
    elif obj_level == "3": 
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)
        obj_l3 = UserGroup.objects.get(name=obj_AuditFlow.l3)  
        if obj_l1 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="1",user_l1=login_user,updated_at_l1=time_now)
        if obj_l2 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="5",user_l2=login_user,updated_at_l2=time_now)
        if obj_l3 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="7",user_l3=login_user,updated_at_l3=time_now)

    return HttpResponse(u'成功')

@login_required()
@permission_verify()
def TaskStatus_deny(request):
#     temp_name = "skdeploy/skdeploy-header.html"
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   
    TaskStatus_id = request.GET.get('id', '')
    login_user = request.user
  
    login_user = str(login_user)
   
    
    obj_user = UserInfo.objects.get(username=request.user)    
    obj_group = obj_user.usergroup_set.all()
    
    
    obj_TaskStatus = TaskStatus.objects.get(id=TaskStatus_id)
    obj_Project = Project.objects.get(id=obj_TaskStatus.project_id)

    obj_AuditFlow = AuditFlow.objects.get(name = obj_Project.audit_flow)
  
    
    obj_level = obj_AuditFlow.level
    if obj_level == "1":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        if obj_l1 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="2",user_l1=login_user,updated_at_l1=time_now)
            
    elif obj_level == "2":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)   
        if obj_l1 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="2",user_l1=login_user,updated_at_l1=time_now)
        if obj_l2 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="6",user_l2=login_user,updated_at_l2=time_now)
            
    elif obj_level == "3": 
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)
        obj_l3 = UserGroup.objects.get(name=obj_AuditFlow.l3)  
        if obj_l1 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="2",user_l1=login_user,updated_at_l1=time_now)
        if obj_l2 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="6",user_l2=login_user,updated_at_l2=time_now)
        if obj_l3 in obj_group:
            TaskStatus.objects.filter(id=TaskStatus_id).update(status="8",user_l3=login_user,updated_at_l3=time_now)

    return HttpResponse(u'成功')   