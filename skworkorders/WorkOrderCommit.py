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

from git  import Git,Repo
from skaccounts.models import UserInfo,UserGroup,AuditFlow
from lib.lib_ansible import get_AnsibleHostsList,get_ansible_config_var
from django import forms
from lib.lib_redis import RedisLock
from dwebsocket.decorators import accept_websocket, require_websocket
import subprocess
from lib_skworkorders import get_VarsGroup_form,var_change2,format_to_user_vars,custom_task,permission_submit_pass
from django.db.models import Count 



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
    tpl_all = WorkOrder.objects.filter(user_dep__in=obj_group,status="yes",template_enable = False).distinct()
    tpl_env = Environment.objects.all()
    tpl_dic_obj={}
    tpl_dic_obj["ALL"]=tpl_all
    for e in tpl_env:
        obj = WorkOrder.objects.filter(user_dep__in=obj_group,status="yes",template_enable = False,env=e.id).distinct()

        tpl_dic_obj[e.name_english]=obj
    print tpl_dic_obj
  
        

    
   
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

@login_required()
@permission_verify()
def WorkOrderCommit_add(request, ids):
    temp_name = "skworkorders/skworkorders-header.html"
    status = 0
    obj = get_object(WorkOrder, id=ids)
    obj_title = str(obj.name) + "-" + str(obj.env)
    obj_audit = obj.audit_flow
    user = request.user
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
        if permission_submit_pass(user, WorkOrder_id=ids):
            tpl_WorkOrderCommit_form = WorkOrderCommit_form(initial=dic_init)  
            if obj.var_opional: 
                tpl_custom_form_list = get_VarsGroup_form(obj.var_opional)
            if obj.audit_enable == False:
                tpl_WorkOrderCommit_form.fields["desc"].widget=forms.HiddenInput()
            
        
            return render_to_response("skworkorders/WorkOrderCommit_add.html", locals(), RequestContext(request))
        else:
            response_data = {}  
            response_data['result'] = 'failed'  
            response_data['message'] = 'You donot have permisson' 
            return HttpResponse(json.dumps(response_data), content_type="application/json")  

            


    
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
            print "message_dic:%s" %    message_dic
            WorkOrder_id = int(message_dic['id'])
            user = request.user
            if permission_submit_pass(user, WorkOrder_id):
                obj_WorkOrder = get_object(WorkOrder, id=WorkOrder_id)  
                user_vars_dic = format_to_user_vars(**message_dic)
                if obj_WorkOrder.pre_task:
                    custom_task(obj_WorkOrder, user_vars_dic, request,taskname="pre_task")
                
                
                if obj_WorkOrder.audit_enable == False:
                    if obj_WorkOrder.main_task:
                        retcode = custom_task(obj_WorkOrder, user_vars_dic, request,taskname="main_task")
    
                    if obj_WorkOrder.post_task:
                        retcode = custom_task(obj_WorkOrder, user_vars_dic, request,taskname="post_task")
                        
                    obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    user_vars_dic["finished_at"]=obj_finished_at
                    if retcode == 0:
                        user_vars_dic["status"] = 3
                        WorkOrderFlow.objects.create(**user_vars_dic)
                        request.websocket.send("finished:工单执行成功")
                    else:
                        user_vars_dic["status"] = 4
                        WorkOrderFlow.objects.create(**user_vars_dic)
                        request.websocket.send("finished:工单执行失败")
                    
                else:
                    obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    user_vars_dic["finished_at"]=obj_finished_at
                    user_vars_dic["status"] = 0
                    WorkOrderFlow.objects.create(**user_vars_dic)
                    request.websocket.send("finished:工单提交成功")
               
            else:
                response_data = {}  
                response_data['result'] = 'failed'  
                response_data['message'] = 'finished:You donot have permisson' 
                request.websocket.send(json.dumps(response_data))
# 
# @login_required()
# @permission_verify()
# @accept_websocket
# def pretask(request):
#     temp_name = "skworkorders/skworkorders-header.html" 
#     if not request.is_websocket():#判断是不是websocket连接
#        
#         try:#如果是普通的http方法
#             message = request.GET['message']
#             return HttpResponse(message)
#         except:
#             return render_to_response('skworkorders/websocket.html', locals(), RequestContext(request))
#     else:
#         for message in request.websocket:
#             
#             message_dic = eval(message)
#             
#             WorkOrder_id = int(message_dic['id'])
#             
#             obj = get_object(WorkOrder, id=WorkOrder_id)
#             pre_task = var_change2(obj.pre_task,**message_dic) 
#             var_built_in_dic = eval(obj.var_built_in) 
#           
#             pre_task = var_change2(pre_task,**var_built_in_dic)
#             
#             pre_task_list = pre_task.encode("utf-8").split("\r")
#       
#         
#             for cmd in pre_task_list:
#              
#                 pcmd = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
#                 while True: 
#                     line = pcmd.stdout.readline().strip()  #获取内容
#                     
#                     if line:
#                         request.websocket.send(line)
#                     else:    
#                         break
#                 retcode=pcmd.wait()
#                 if retcode==0:
#                     pass
#                 else:
#                     ret_message="执行失败"
#                     break
#             if retcode==0:
#                 ret_message="执行成功"
#             message_dic = format_to_user_vars(**message_dic)
#             print "xxx:%s" % message_dic
#             WorkOrderFlow.objects.create(**message_dic)
#             request.websocket.send(ret_message)
