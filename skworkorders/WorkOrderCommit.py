#! /usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse
from models import AuditFlow,Environment,WorkOrder,WorkOrderFlow
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from .forms import WorkOrderCommit_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
from datetime import datetime
import json
from skaccounts.models import UserInfo
from django import forms
from dwebsocket.decorators import accept_websocket

from skworkorders.lib_skworkorders import get_VarsGroup_form,format_to_user_vars,custom_task,permission_submit_pass
from lib.lib_json import my_obj_pairs_hook

from datetime import datetime,timedelta
import pytz
from skworkorders import tasks
from skipper.celery import app as celery_app



import logging
log = logging.getLogger('skworkorders')


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
 
    if permission_submit_pass(user, WorkOrder_id=ids):
        tpl_WorkOrderCommit_form = WorkOrderCommit_form(initial=dic_init)  
        if obj.var_opional_switch == True and obj.var_opional: 
            tpl_custom_form_list = get_VarsGroup_form(obj.var_opional)
        if obj.audit_enable == False:
            tpl_WorkOrderCommit_form.fields["desc"].widget=forms.HiddenInput()
        if obj.schedule_enable == False:
            tpl_WorkOrderCommit_form.fields["celery_schedule_time"].widget=forms.HiddenInput()
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
            request.websocket.send("开始提交任务,请耐心等待·······")
            message_dic = json.loads(message,object_pairs_hook=my_obj_pairs_hook)
            WorkOrder_id = int(message_dic['id'])
            user = request.user
            
            if permission_submit_pass(user, WorkOrder_id):
                obj_WorkOrder = get_object(WorkOrder, id=WorkOrder_id)  
                log.error("User:%s,Env:%s,WorkOrderName:%s commit starting" % (user,obj_WorkOrder.env,obj_WorkOrder.name)) 
                message_dic_format,user_vars_dic = format_to_user_vars(**message_dic)
                if obj_WorkOrder.pre_task:
                    retcode = custom_task(obj_WorkOrder, user_vars_dic, request,taskname="pre_task")
                else:
                    retcode = 0

                if retcode == 0 and obj_WorkOrder.audit_enable == False and obj_WorkOrder.schedule_enable == False:
                    log.info("User:%s,Env:%s,WorkOrderName:%s execute starting" % (user,obj_WorkOrder.env,obj_WorkOrder.name))
                    if obj_WorkOrder.main_task:
                        retcode = custom_task(obj_WorkOrder, user_vars_dic, request,taskname="main_task")
    
                    if obj_WorkOrder.post_task and retcode==0:
                        retcode = custom_task(obj_WorkOrder, user_vars_dic, request,taskname="post_task")
                        
                    obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    message_dic_format["finished_at"]=obj_finished_at
                    if retcode == 0:
                        message_dic_format["status"] = 3
                        WorkOrderFlow.objects.create(**message_dic_format)
                        request.websocket.send("finished:工单执行成功")
                        log.info("User:%s,Env:%s,WorkOrderName:%s finished:successful工单执行成功" % (user,obj_WorkOrder.env,obj_WorkOrder.name)) 
                    else:
                        message_dic_format["status"] = 4
                        WorkOrderFlow.objects.create(**message_dic_format)
                        request.websocket.send("finished:工单执行失败")
                        log.error("User:%s,Env:%s,WorkOrderName:%s finished:failed工单执行失败" % (user,obj_WorkOrder.env,obj_WorkOrder.name))
                        
              
                elif retcode == 0 and obj_WorkOrder.audit_enable == False and obj_WorkOrder.schedule_enable == True:
                    request.websocket.send("开始提交定时任务")
                    time01 = message_dic_format["celery_schedule_time"]
                    if time01 == "":
                        request.websocket.send("warning:请输入计划执行时间")
                    else:
                        time01 = datetime.strptime(time01, "%Y-%m-%d-%H:%M:%S")
                        local_tz = pytz.timezone(celery_app.conf['CELERY_TIMEZONE'])
                        format_eta = local_tz.localize(datetime.strptime(str(time01).strip(), '%Y-%m-%d %H:%M:%S'))
                        taskname_dic = {"main_task":obj_WorkOrder.main_task,"post_task":obj_WorkOrder.post_task}
                        print "taskname_dic: %s" % taskname_dic
                        if obj_WorkOrder.var_built_in:
                            var_built_in_dic = eval(obj_WorkOrder.var_built_in) 
                        else:
                            var_built_in_dic = {}
                        task01 = tasks.schedule_task.apply_async((taskname_dic,var_built_in_dic,user_vars_dic), eta=format_eta)
                        message_dic_format["celery_task_id"]=task01.id    
                        message_dic_format["status"] = "PENDING"
                        message_dic_format["celery_schedule_time"] = time01
                        
                        WorkOrderFlow.objects.create(**message_dic_format)
                        request.websocket.send("finished:提交定时任务成功")
                        log.info("User:%s,Env:%s,WorkOrderName:%s finished:successful定时任务添加成功" % (user,obj_WorkOrder.env,obj_WorkOrder.name))
                 
                        
                
                
                
                elif retcode == 0 and obj_WorkOrder.audit_enable == True and obj_WorkOrder.schedule_enable == False:                 
                    message_dic_format["status"] = 0
                    WorkOrderFlow.objects.create(**message_dic_format)
                    request.websocket.send("finished:工单提交成功")
                    log.info("User:%s,Env:%s,WorkOrderName:%s finished:successful工单提交成功" % (user,obj_WorkOrder.env,obj_WorkOrder.name))
                    
                elif retcode == 0 and obj_WorkOrder.audit_enable == True and obj_WorkOrder.schedule_enable == True: 
                    time01 = message_dic_format["celery_schedule_time"] 
                    if time01 == "":
                        request.websocket.send("warning:请输入计划执行时间")
                    else:
                        time01 = datetime.strptime(time01, "%Y-%m-%d-%H:%M:%S")                
                        message_dic_format["status"] = 0
                        message_dic_format["celery_schedule_time"] = time01
                        WorkOrderFlow.objects.create(**message_dic_format)
                        request.websocket.send("finished:工单提交成功")
                        log.info("User:%s,Env:%s,WorkOrderName:%s finished:successful工单提交成功" % (user,obj_WorkOrder.env,obj_WorkOrder.name))
                else:
                    request.websocket.send("finished:工单提交失败")
                    log.warning("User:%s,Env:%s,WorkOrderName:%s finished:successful工单提交失败" % (user,obj_WorkOrder.env,obj_WorkOrder.name))
                        
               
            else:
                response_data = {}  
                response_data['result'] = 'failed'  
                response_data['message'] = 'finished:You donot have permisson' 
                request.websocket.send(json.dumps(response_data))
                log.warning(response_data)
        
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
