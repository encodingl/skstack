#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,Environment,WorkOrderGroup,WorkOrder,WorkOrderFlow
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log
from .forms import WorkOrderFlow_detail_form,WorkOrderFlow_release_form,WorkOrderFlow_rollback_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime
from lib_skworkorders import adv_task_step, release_project,uni_to_str
import redis
from lib.lib_config import get_redis_config
from lib.file import get_ex_link

import time
from skaccounts.models import UserInfo,UserGroup
from django.db.models import Q
from itertools import chain
from django.db.models import Max
from lib.lib_redis import RedisLock


@login_required()
@permission_verify()
def WorkOrderFlow_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    
    tpl_all = WorkOrderFlow.objects.filter(user_commit=request.user)
#     obj_user = UserInfo.objects.get(username=request.user)    
#     obj_group = obj_user.usergroup_set.all()
#   
#     obj_AuditFlow = AuditFlow.objects.filter(Q(l1__in=obj_group)|Q(l2__in=obj_group)|Q(l3__in=obj_group))
#     obj_workorder = WorkOrder.objects.filter(audit_flow__in = obj_AuditFlow)
#     obj_workorder_audit = WorkOrderFlow.objects.filter(workorder_id__in=obj_workorder)
# 
#     tpl_all = list(chain(obj_user_commit, obj_workorder_audit))
#     tpl_all = list(set(tpl_all))
   
    return render_to_response('skworkorders/WorkOrderFlow_index.html', locals(), RequestContext(request))



 
 
@login_required()
@permission_verify()
def WorkOrderFlow_revoke(request):
#     temp_name = "skworkorders/skworkorders-header.html"
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    WorkOrderFlow_id = request.GET.get('id', '')
    obj=WorkOrderFlow.objects.get(id=WorkOrderFlow_id)
    obj_workorder=obj.workorder
    obj_env=obj.env
    obj_workorder_id=obj.workorder_id
     
    redis_chanel = obj_workorder + obj_env
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
     
    redis_chanel_taskcommit_lock = redis_chanel + obj_workorder_id + "_taskcommit_lock"
     
     
    if WorkOrderFlow_id:
        WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="9",finished_at=time_now)
        conn.set(redis_chanel_taskcommit_lock,"0")
         
     
    if request.method == 'POST':
        WorkOrderFlow_items = request.POST.getlist('x_check', [])
        if WorkOrderFlow_items:
            for n in WorkOrderFlow_items:
                WorkOrderFlow.objects.filter(id=n).update(status="9",finished_at=time_now)
                conn.set(redis_chanel_taskcommit_lock,"0")
    return HttpResponse(u'撤销成功')
 
 
 
@login_required()
@permission_verify()
def WorkOrderFlow_detail(request, ids):
     
    obj = get_object(WorkOrderFlow, id=ids)
    tpl_WorkOrderFlow_form = WorkOrderFlow_detail_form(instance=obj) 
    
    return render_to_response("skworkorders/WorkOrderFlow_detail.html", locals(), RequestContext(request))
 
 
@login_required()
@permission_verify()
def WorkOrderFlow_release(request, ids):
    temp_name = "skworkorders/skworkorders-header.html"
    obj = get_object(WorkOrderFlow, id=ids) 
    obj_title=obj.title
    if obj_title.endswith('-rollback'):
        dic_init={'workorder':obj.workorder,
              'workorder_id':obj.workorder_id,          
             'env':obj.env,
             'desc':obj.desc,
             
             }
        tpl_WorkOrderFlow_release_form = WorkOrderFlow_rollback_form(initial=dic_init)  
        return render_to_response("skworkorders/WorkOrderFlow_rollback.html", locals(), RequestContext(request))
     
    else:
        dic_init={'workorder':obj.workorder,
                  'workorder_id':obj.workorder_id,          
                 'env':obj.env,
                 'commit_id':obj.commit_id, 
                 'forks':obj.forks,            
                 }
        tpl_WorkOrderFlow_release_form = WorkOrderFlow_release_form(initial=dic_init)  
        return render_to_response("skworkorders/WorkOrderFlow_release.html", locals(), RequestContext(request))
 
 
 
  
     
     
 
@login_required()
@permission_verify()
def WorkOrderFlow_release_run(request):
    """release步骤发布视图函数
    主要分为如下几个部分：
    1 判断是否通过审核，只有通过审核后才能进行上线
    2 判断是否重复执行，一个环境中的一个项目只同时发布一次
    3 同步项目文件
    4 执行pre-release步骤脚本
    5 修改目标实例项目运行目录软链接
    6 执行post-release步骤脚本
    """
    WorkOrderFlow_id = request.POST.get('id')
   
    if WorkOrderFlow_id:
        obj = WorkOrderFlow.objects.get(id=WorkOrderFlow_id)
    obj_workorder = obj.workorder
 
    obj_env = obj.env
    obj_workorder_id = obj.workorder_id
    obj_status = obj.status
    obj_audit_level = obj.audit_level
    obj_forks = obj.forks
     
     
     
    obj2 = WorkOrder.objects.get(id=obj_workorder_id)
    if obj.hosts_cus:
         
        obj_hosts = uni_to_str(obj.hosts_cus)
    else:
        obj_hosts = obj2.hosts 
         
    print obj_hosts
    now_time = time.strftime("%Y%m%d-%H%M%S")
  
    if obj2.release_library.endswith('/'):
    
        obj_release_dir = obj2.release_library + obj_workorder + "/" + now_time + "/" 
    else:
        obj_release_dir = obj2.release_library + "/" + obj_workorder + "/" + now_time
    obj_release_to = obj2.release_to
#     obj_ex_link_id = get_ex_link(hosts=obj_hosts,dir=obj2.release_to)
    obj3 = WorkOrderFlow.objects.filter(title=obj.title,status="3").aggregate(Max('link_id'))
    obj_ex_link_id = obj3["link_id__max"]
   
    redis_chanel = obj_workorder + obj_env
    redis_chanel_message = redis_chanel+"message"
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
    redis_chanel_taskrelease_lock = redis_chanel + obj_workorder_id + "_taskrelease_lock"
    redis_chanel_taskcommit_lock = redis_chanel + obj_workorder_id + "_taskcommit_lock"
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
    if conn.get(redis_chanel_taskrelease_lock == "1") :
        conn.set(redis_chanel_message,"You have already submitted, or someone else is submitting the same workorder.ny other problems, please contact the administrator")     
        conn.set(redis_chanel,"2")        
        ret=conn.get(redis_chanel_message)
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)
         
    else:
        conn.set(redis_chanel_taskrelease_lock,"1")
 
# 步骤3 同步workorder文件
    result_release_workorder = release_workorder(workorder=obj_workorder,env=obj_env,hosts=obj_hosts,release_dir=obj_release_dir,release_to=obj_release_to)
    if result_release_workorder == "success": 
        result_release_workorder = "file sync task %s" % result_release_workorder
        conn.set(redis_chanel_message,result_release_workorder)     
        conn.set(redis_chanel,"25") 
    else:
        conn.set(redis_chanel,"5")
        ret=conn.get(redis_chanel_message)
        result_release_workorder = "file sync  task %s" % result_release_workorder
        conn.set(redis_chanel_message,result_release_workorder) 
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="4",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at)
        obj_json = json.dumps(ret)
        conn.set(redis_chanel_taskrelease_lock,"0")
        conn.set(redis_chanel_taskcommit_lock,"0")
        return  HttpResponse(obj_json)    
   
  
     
# 步骤4 执行pre release任务
    result_pre_release = adv_task_step(hosts=obj_hosts, env=obj_env, workorder=obj_workorder, task_file="pre_release.sh")
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
        WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="4",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at)
        obj_json = json.dumps(ret)
        conn.set(redis_chanel_taskrelease_lock,"0")
        conn.set(redis_chanel_taskcommit_lock,"0")
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
        WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="4",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at) 
        obj_json = json.dumps(ret)
        conn.set(redis_chanel_taskrelease_lock,"0")
        conn.set(redis_chanel_taskcommit_lock,"0")
        return  HttpResponse(obj_json) 
# 步骤6 执行post release任务
    result_post_release = adv_task_step(hosts=obj_hosts, env=obj_env, workorder=obj_workorder, task_file="post_release.sh",forks=obj_forks)
    if result_post_release == "success": 
        result_post_release = "post_release task %s" % result_post_release
        conn.set(redis_chanel_message,result_post_release)     
        conn.set(redis_chanel,"100") 
        ret="ok"
        obj_json = json.dumps(ret)
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="3",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at)
        result_post_release=conn.get(redis_chanel_message)
     
        conn.set(redis_chanel_taskrelease_lock,"0")
        conn.set(redis_chanel_taskcommit_lock,"0")
        return  HttpResponse(obj_json)
    else:
        conn.set(redis_chanel,"80")
        ret=conn.get(redis_chanel_message)
        result_post_release = "post_release task %s" % result_post_release
        conn.set(redis_chanel_message,result_post_release) 
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="4",link_id=obj_release_dir,ex_link_id=obj_ex_link_id,finished_at=obj_finished_at)
        obj_json = json.dumps(ret)
        conn.set(redis_chanel_taskrelease_lock,"0")
        conn.set(redis_chanel_taskcommit_lock,"0")
        return  HttpResponse(obj_json)    
     
  
     
 
 
 
@login_required()
@permission_verify()
def WorkOrderFlow_release_status(request):
    WorkOrderFlow_id = request.POST.get('id') 
    obj = WorkOrderFlow.objects.get(id=WorkOrderFlow_id)
    obj_workorder = obj.workorder
    obj_env = obj.env 
    redis_chanel=obj_workorder+obj_env
     
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
    else:
        pass
    return  HttpResponse(obj_json) 
 
 
@login_required()
@permission_verify()
def WorkOrderFlow_rollback_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    WorkOrderFlow_id = request.GET.get('id', '')
    obj = get_object(WorkOrderFlow, id=WorkOrderFlow_id) 
    obj_title = str(obj.workorder) + "-" + str(obj.env) + "-" + "rollback"
    obj_status = 3
    obj_desc = "The original task id " + str(obj.id) + " rollback:" + "\nfrom: " + str(obj.link_id) + "\nto: " + str(obj.ex_link_id)
    dic_rollback={
             'title':obj_title,
             'workorder':obj.workorder,
             'workorder_id':obj.workorder_id,          
             'env':obj.env,
             'link_id':obj.ex_link_id,
             'commit_id':obj.commit_id,
             'workorder_group':obj.workorder_group,
             'branch':obj.branch,
             'desc':obj_desc,
             'status':"0",
             'user_commit':request.user,
              
             }
 
    WorkOrderFlow.objects.create(**dic_rollback)
    tpl_all = WorkOrderFlow.objects.all()
    return render_to_response("skworkorders/WorkOrderFlow_index.html", locals(), RequestContext(request))
 
 
 
 
     
     
@login_required()
@permission_verify()
def WorkOrderFlow_history(request):
    temp_name = "skworkorders/skworkorders-header.html"    
     
    tpl_all = WorkOrderFlow.objects.all()
   
    
    return render_to_response('skworkorders/WorkOrderFlow_history.html', locals(), RequestContext(request))
 
 
@login_required()
@permission_verify()
def WorkOrderFlow_audit(request):
    temp_name = "skworkorders/skworkorders-header.html"    
     
#     obj_user_commit = WorkOrderFlow.objects.filter(user_commit=request.user)
    obj_user = UserInfo.objects.get(username=request.user)    
    obj_group = obj_user.usergroup_set.all()
   
    obj_AuditFlow = AuditFlow.objects.filter(Q(l1__in=obj_group)|Q(l2__in=obj_group)|Q(l3__in=obj_group))
    obj_workorder = WorkOrder.objects.filter(audit_flow__in = obj_AuditFlow,audit_enable=True)
    tpl_all = WorkOrderFlow.objects.filter(workorder_id__in=obj_workorder)
 
#     tpl_all = list(chain(obj_user_commit, obj_workorder_audit))
#     tpl_all = list(set(tpl_all))
    
    return render_to_response('skworkorders/WorkOrderFlow_audit.html', locals(), RequestContext(request))
 
@login_required()
@permission_verify()
def WorkOrderFlow_permit(request):
#     temp_name = "skworkorders/skworkorders-header.html"
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
    WorkOrderFlow_id = request.GET.get('id', '')
    login_user = request.user  
    login_user = str(login_user) 
    obj_user = UserInfo.objects.get(username=request.user)    
    obj_group = obj_user.usergroup_set.all()  
    
    obj_WorkOrderFlow = WorkOrderFlow.objects.get(id=WorkOrderFlow_id)
    obj_WorkOrder = WorkOrder.objects.get(id=obj_WorkOrderFlow.workorder_id)
    obj_AuditFlow = AuditFlow.objects.get(name = obj_WorkOrder.audit_flow)   
    obj_level = obj_AuditFlow.level
    obj_status = obj_WorkOrderFlow.status
    
    obj_workorder = str(obj_WorkOrder.name)
    obj_env = str(obj_WorkOrder.env)
    obj_workorder_id = str(obj_WorkOrder.id)
    redis_chanel = obj_workorder + obj_env 
    redis_chanel_taskcommit_lock = redis_chanel + obj_workorder_id + "_taskcommit_lock"   
    rlock = RedisLock(channel_name = redis_chanel_taskcommit_lock)
     
    if obj_level == "1":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        if obj_l1 in obj_group:
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="1",user_l1=login_user,updated_at_l1=time_now)
        rlock.lock()
             
    elif obj_level == "2":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
     
        obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)  
     
        if obj_l1 in obj_group and (obj_status == "0" or obj_status == "2"):
          
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="1",user_l1=login_user,updated_at_l1=time_now)
        if obj_l2 in obj_group :
       
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="5",user_l2=login_user,updated_at_l2=time_now)
        rlock.lock()
             
    elif obj_level == "3" and (obj_status == "0" or obj_status == "2" or obj_status == "6" or obj_status == "8"): 
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)
        obj_l3 = UserGroup.objects.get(name=obj_AuditFlow.l3)  
        if obj_l1 in obj_group and (obj_status == "0" or obj_status == "2"):
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="1",user_l1=login_user,updated_at_l1=time_now)
        if obj_l2 in obj_group and (obj_status == "0" or obj_status == "2" or obj_status == "1" or obj_status == "6"):
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="5",user_l2=login_user,updated_at_l2=time_now)
        if obj_l3 in obj_group :
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="7",user_l3=login_user,updated_at_l3=time_now)
        rlock.lock()
 
    return HttpResponse(u'ok')
 
@login_required()
@permission_verify()
def WorkOrderFlow_deny(request):
#     temp_name = "skworkorders/skworkorders-header.html"
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    WorkOrderFlow_id = request.GET.get('id', '')
    login_user = request.user
   
    login_user = str(login_user)
    
     
    obj_user = UserInfo.objects.get(username=request.user)    
    obj_group = obj_user.usergroup_set.all()
     
     
    obj_WorkOrderFlow = WorkOrderFlow.objects.get(id=WorkOrderFlow_id)
    obj_status = obj_WorkOrderFlow.status
    obj_WorkOrder = WorkOrder.objects.get(id=obj_WorkOrderFlow.workorder_id)
 
    obj_AuditFlow = AuditFlow.objects.get(name = obj_WorkOrder.audit_flow)
   
     
    obj_level = obj_AuditFlow.level
    if obj_level == "1":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        if obj_l1 in obj_group:
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="2",user_l1=login_user,updated_at_l1=time_now)
             
    elif obj_level == "2":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)   
        if obj_l1 in obj_group and (obj_status == "0" or obj_status == "1"):
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="2",user_l1=login_user,updated_at_l1=time_now)
        if obj_l2 in obj_group:
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="6",user_l2=login_user,updated_at_l2=time_now)
             
    elif obj_level == "3": 
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)
        obj_l3 = UserGroup.objects.get(name=obj_AuditFlow.l3)  
        if obj_l1 in obj_group and (obj_status == "0" or obj_status == "1"):
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="2",user_l1=login_user,updated_at_l1=time_now)
        if obj_l2 in obj_group and (obj_status == "0" or obj_status == "2" or obj_status == "1" or obj_status == "5"):
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="6",user_l2=login_user,updated_at_l2=time_now)
        if obj_l3 in obj_group:
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="8",user_l3=login_user,updated_at_l3=time_now)
    obj_workorder = str(obj_WorkOrder.name)
    obj_env = str(obj_WorkOrder.env)
    obj_workorder_id = str(obj_WorkOrder.id)
    redis_chanel = obj_workorder + obj_env
    redis_chanel_taskcommit_lock = redis_chanel + obj_workorder_id + "_taskcommit_lock"
    rlock = RedisLock(channel_name = redis_chanel_taskcommit_lock)
    rlock.unlock()
 
    return HttpResponse(u'成功')   