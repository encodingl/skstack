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
from lib.lib_git import get_git_taglist, get_git_commitid
from .forms import WorkOrderCommit_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime

import redis
import time
import json
from lib.lib_config import get_redis_config
from lib_skworkorders import adv_task_step,get_VarsGroup_form,var_change2
from git  import Git,Repo
from skaccounts.models import UserInfo,UserGroup,AuditFlow
from lib.lib_ansible import get_AnsibleHostsList,get_ansible_config_var
from django import forms
from lib.lib_redis import RedisLock
from dwebsocket.decorators import accept_websocket, require_websocket
import subprocess



level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)
git_path = get_dir("git_path")


@login_required()
@permission_verify()
def WorkOrderCommit_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
 
    obj_user = UserInfo.objects.get(username=request.user)
    
    obj_group = obj_user.usergroup_set.all()
    obj_workorder = WorkOrder.objects.filter(user_dep__in=obj_group,status="yes",template_enable = False)
    tpl_all = obj_workorder
   
    return render_to_response('skworkorders/WorkOrderCommit_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrderCommit_undo(request):
#    temp_name = "skworkorders/skworkorders-header.html"
    WorkOrderCommit_id = request.GET.get('id', '')
    if WorkOrderCommit_id:
        WorkOrderFlow.objects.filter(id=WorkOrderCommit_id).delete()
    
    if request.method == 'POST':
        WorkOrderCommit_items = request.POST.getlist('x_check', [])
        if WorkOrderCommit_items:
            for n in WorkOrderCommit_items:
                WorkOrderFlow.objects.filter(id=n).delete()
    return HttpResponse(u'撤销成功')
 #   allworkorder = TaskCommit.objects.all()
    
 #   return render_to_response("skworkorders/TaskCommit.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrderCommit_add(request, ids):
    temp_name = "skworkorders/skworkorders-header.html"
    status = 0
    obj = get_object(WorkOrder, id=ids)
    
    obj_title = str(obj.name) + "-" + str(obj.env)
    obj_audit = obj.audit_flow
    if not obj_audit:
        obj_level = "0" 
    else:
        obj_level = AuditFlow.objects.get(name=obj_audit).level
    dic_init={'title':obj_title,
              'workorder':obj.name,
              'workorder_id':obj.id,
             'workorder_group':obj.group,
             'env':obj.env,
             'user_commit':request.user,   
             'status':"0",
             'audit_level':obj_level,            
             
             }
    
    if request.method == 'POST':
        tpl_WorkOrderCommit_form = WorkOrderCommit_form(request.POST)
        
        
        if tpl_WorkOrderCommit_form.is_valid():
    
            tpl_WorkOrderCommit_form.save()
            ret = []
            message = "SUCCESS\nWorkOrder:%s\n Env:%s\n提单成功" % (obj.name,obj.env)
            ret.append(message)
            return render_to_response("skworkorders/WorkOrderCommit_result.html", locals(), RequestContext(request))
        else:
            
            pass
                
            return render_to_response("skworkorders/WorkOrderCommit_add.html", locals(), RequestContext(request))
    else:  
        tpl_WorkOrderCommit_form = WorkOrderCommit_form(initial=dic_init)  
        if obj.var_opional: 
            tpl_custom_form_list = get_VarsGroup_form(obj.var_opional)
        
    
        return render_to_response("skworkorders/WorkOrderCommit_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def WorkOrderCommit_check(request):
    obj_env=request.POST.get('env') 
    
    obj_workorder = request.POST.get('workorder')  
    obj_workorder_id = request.POST.get('workorder_id')
    
    
    redis_chanel = obj_workorder + obj_env
    redis_chanel_message = redis_chanel+"message"
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
    redis_chanel_taskcommit_lock = str(redis_chanel) + str(obj_workorder_id) + "_taskcommit_lock"
  
   
    
#若存在已提单但未发布的项目，必须撤销或者发布后才能新建提交     
    if conn.get(redis_chanel_taskcommit_lock) == "1" :
        conn.set(redis_chanel_message,"failed ,存在已提单但未发布的项目，必须撤销或者发布后才能新建提交")     
        conn.set(redis_chanel,"5")        
        ret=conn.get(redis_chanel_message)
     
        obj_json = json.dumps(ret)
        return  HttpResponse(obj_json)
    else :
        
    
        result_pre_deploy = adv_task_step(hosts="localhost", env=obj_env, workorder=obj_workorder, task_file="pre_deploy.sh")  
      
        if result_pre_deploy == "success": 
            result_pre_deploy = "pre_deploy task %s" % result_pre_deploy
            conn.set(redis_chanel_message,result_pre_deploy)     
            conn.set(redis_chanel,"30") 
        else:
            conn.set(redis_chanel,"10")
            ret=conn.get(redis_chanel_message)
            result_pre_deploy = "pre_deploy task %s" % result_pre_deploy
            conn.set(redis_chanel_message,result_pre_deploy) 
            
            obj_json = json.dumps(ret)
            return  HttpResponse(obj_json) 
        
#         result_pre_deploy=conn.get(redis_chanel_message)
       
        if obj_git_commit is not None:  
            obj_path = git_path + obj_env + "/" + obj_workorder  
            g = Git(obj_path)  
            g.checkout(obj_git_commit)
            conn.set(redis_chanel,"60")
            conn.set(redis_chanel_message,"git checkout success")
        
       
    
         
         
        result_post_deploy = adv_task_step(hosts="localhost", env=obj_env, workorder=obj_workorder, task_file="post_deploy.sh")   
        
        if result_post_deploy == "success":     
            conn.set(redis_chanel,"100") 
            result_post_deploy = "post_deploy task %s" % result_post_deploy
            conn.set(redis_chanel_message,result_post_deploy) 
            ret="ok"
            obj_json = json.dumps(ret)
#             result_post_deploy=conn.get(redis_chanel_message)
            
           
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
def WorkOrderCommit_checkstatus(request):
    obj_env=request.POST.get('env') 
    obj_workorder = request.POST.get('workorder')  
    redis_chanel=obj_workorder+obj_env
    redis_chanel_message = redis_chanel+"message"
    ret={}
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
    ret["redis_chanel"]=conn.get(redis_chanel) 
    ret["redis_chanel_message"]=conn.get(redis_chanel_message)
    
    if (ret["redis_chanel_message"] is not None and "failed" in ret["redis_chanel_message"]) or (ret["redis_chanel"] is not None and ret["redis_chanel"])  == "100" :       
        conn.delete(redis_chanel)
        conn.delete(redis_chanel_message)
    obj_json = json.dumps(ret)
   

    return  HttpResponse(obj_json)   

@login_required()
@permission_verify()
@accept_websocket
def pretask(request):
    temp_name = "skworkorders/skworkorders-header.html" 
    if not request.is_websocket():#判断是不是websocket连接
       
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render_to_response('skworkorders/websocket.html', locals(), RequestContext(request))
    else:
        for message in request.websocket:
            
            message_dic = eval(message)
  
            WorkOrder_id = int(message_dic['id'])
            
            obj = get_object(WorkOrder, id=WorkOrder_id)
            pre_task = var_change2(obj.pre_task,**message_dic) 
            var_built_in_dic = eval(obj.var_built_in) 
            pre_task = var_change2(pre_task,**var_built_in_dic)
            print "pretask: %s" % pre_task
            print type(pre_task)
            pre_task_list = pre_task.encode("utf-8").split("\r")
            print type(pre_task_list)
            print "pre_task_list:%s" % pre_task_list
            for cmd in pre_task_list:
                print "cmd:%s" % cmd
                pcmd = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
                while True: 
                     line = pcmd.stdout.readline().strip()  #获取内容
                     
                     if line:
                          request.websocket.send(line)
                     else:    
                         break
                retcode=pcmd.wait()
                if retcode==0:
                    pass
                else:
                    ret_message="执行失败"
                    break
            if retcode==0:
                ret_message="执行成功"
            WorkOrderFlow.objects.create(**message_dic)
            request.websocket.send(ret_message)
