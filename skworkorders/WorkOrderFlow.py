#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from models import AuditFlow,Environment,WorkOrder,WorkOrderFlow

from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify

from .forms import WorkOrderFlow_detail_form,WorkOrderFlow_release_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json


from datetime import datetime


from django.utils import timezone
from datetime import timedelta


from skaccounts.models import UserInfo,UserGroup
from django.db.models import Q

from dwebsocket.decorators import accept_websocket
from lib_skworkorders import custom_task,permission_submit_pass,permission_audit_pass

import logging
log = logging.getLogger('skworkorders')

@login_required()
@permission_verify()
def WorkOrderFlow_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    current_date=timezone.now()
    tpl_all = WorkOrderFlow.objects.filter(user_commit=request.user,created_at__range=(current_date + timedelta(days=-30),current_date))
    tpl_env = Environment.objects.all()
    tpl_dic_obj={}
    tpl_dic_obj["ALL"]=tpl_all
    for e in tpl_env:
        obj = WorkOrderFlow.objects.filter(user_commit=request.user,env=e.name_english,created_at__range=(current_date + timedelta(days=-30),current_date))
        tpl_dic_obj[e.name_english]=obj

    return render_to_response('skworkorders/WorkOrderFlow_index.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def WorkOrderFlow_history(request):
    temp_name = "skworkorders/skworkorders-header.html"  
    current_date=timezone.now()  
    tpl_env = Environment.objects.all()
    tpl_dic_obj={}
    if request.method == 'POST':
        from_date = request.POST.get('from_date', '')
        print from_date
        print type(from_date)
        from_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
       
        to_date = request.POST.get('to_date', '')
        to_date = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
        tpl_all = WorkOrderFlow.objects.filter(created_at__range=(from_date,to_date))
        for e in tpl_env:
            obj = WorkOrderFlow.objects.filter(env=e.name_english,created_at__range=(from_date,to_date))
            tpl_dic_obj[e.name_english]=obj
    else:
    
        tpl_all = WorkOrderFlow.objects.filter(created_at__range=(current_date + timedelta(days=-30),current_date))
        for e in tpl_env:
            obj = WorkOrderFlow.objects.filter(env=e.name_english,created_at__range=(current_date + timedelta(days=-30),current_date))
            tpl_dic_obj[e.name_english]=obj
    
    tpl_dic_obj["ALL"]=tpl_all
    
    return render_to_response('skworkorders/WorkOrderFlow_history.html', locals(), RequestContext(request))
 
 
@login_required()
@permission_verify()
def WorkOrderFlow_revoke(request):
#     temp_name = "skworkorders/skworkorders-header.html"
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    WorkOrderFlow_id = request.GET.get('id', '')
  
    if WorkOrderFlow_id:
        WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="9",finished_at=time_now)
  
    if request.method == 'POST':
        WorkOrderFlow_items = request.POST.getlist('x_check', [])
        if WorkOrderFlow_items:
            for n in WorkOrderFlow_items:
                WorkOrderFlow.objects.filter(id=n).update(status="9",finished_at=time_now)
               
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
    dic_init={'workorder':obj.workorder,
                  'desc':obj.desc,          
                 'env':obj.env,
                 'user_vars':obj.user_vars,            
                 }
    tpl_WorkOrderFlow_release_form = WorkOrderFlow_release_form(initial=dic_init)  
    return render_to_response("skworkorders/WorkOrderFlow_release.html", locals(), RequestContext(request))
 
 
 
  
     
     
 
@login_required()
@permission_verify()
@accept_websocket
def WorkOrderFlow_release_run(request):
    temp_name = "skworkorders/skworkorders-header.html" 
    if not request.is_websocket():#判断是不是websocket连接
       
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render_to_response('skworkorders/websocket.html', locals(), RequestContext(request))
    else:
        for message in request.websocket:
            WorkOrderFlow_id = int(message)
           
            obj = get_object(WorkOrderFlow, id=WorkOrderFlow_id)     
            obj_WorkOrder = get_object(WorkOrder, id=obj.workorder_id)
         
            user_vars_dic = eval(obj.user_vars)
            user = request.user
            log.info("User:%s,Env:%s,WorkOrderName:%s,WorkOrderFlowID:%s execute starting" % (user,obj_WorkOrder.env,obj_WorkOrder.name,WorkOrderFlow_id)) 
            if permission_audit_pass(obj_audit_level=obj.audit_level,obj_status= obj.status):
                
                if permission_submit_pass(user, WorkOrder_id=obj.workorder_id):
                    
                    if obj_WorkOrder.main_task:
                        retcode = custom_task(obj_WorkOrder, user_vars_dic, request,taskname="main_task")
    
                    if obj_WorkOrder.post_task and retcode==0:
                        retcode = custom_task(obj_WorkOrder, user_vars_dic, request,taskname="post_task")
                    obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if retcode == 0:
                        WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="3",finished_at=obj_finished_at)
                        request.websocket.send("finished:工单执行成功")
                        log.info("User:%s,Env:%s,WorkOrderName:%s,WorkOrderFlowID:%s finished:successful工单执行成功" % (user,obj_WorkOrder.env,obj_WorkOrder.name,WorkOrderFlow_id)) 
                        
                    else:
                        WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="4",finished_at=obj_finished_at)
                        request.websocket.send("finished:工单执行失败")
                        log.error("User:%s,Env:%s,WorkOrderName:%s,WorkOrderFlowID:%s finished:failed工单执行失败" % (user,obj_WorkOrder.env,obj_WorkOrder.name,WorkOrderFlow_id)) 
                   
           
                    
                else:
                    response_data = {}  
                    response_data['result'] = 'failed'  
                    response_data['message'] = 'You donot have permisson' 
                    request.websocket.send(json.dumps(response_data))
                    log.warning(response_data)
            else:
                response_data = {}  
                response_data['result'] = 'failed'  
                response_data['message'] = 'Illegal execution, the work order has not yet been approved' 
                request.websocket.send(json.dumps(response_data))
                log.warning(response_data)
                

   
 
 

     
     

 
 
@login_required()
@permission_verify()
def WorkOrderFlow_audit(request):
    temp_name = "skworkorders/skworkorders-header.html"    
     
#     obj_user_commit = WorkOrderFlow.objects.filter(user_commit=request.user)
    obj_user = UserInfo.objects.get(username=request.user)    
    obj_group = obj_user.usergroup_set.all()
   
    obj_AuditFlow = AuditFlow.objects.filter(Q(l1__in=obj_group)|Q(l2__in=obj_group)|Q(l3__in=obj_group))
    obj_workorder = WorkOrder.objects.filter(audit_flow__in = obj_AuditFlow,audit_enable=True)
    current_date=timezone.now()
   
    tpl_all = WorkOrderFlow.objects.filter(workorder_id__in=obj_workorder,created_at__range=(current_date + timedelta(days=-30),current_date))
    
    tpl_env = Environment.objects.all()
    tpl_dic_obj={}
    tpl_dic_obj["ALL"]=tpl_all
    for e in tpl_env:
        obj = WorkOrderFlow.objects.filter(workorder_id__in=obj_workorder,env=e.name_english,created_at__range=(current_date + timedelta(days=-30),current_date))
        tpl_dic_obj[e.name_english]=obj

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
    

    
     
    if obj_level == "1":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
        if obj_l1 in obj_group:
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="1",user_l1=login_user,updated_at_l1=time_now)
      
             
    elif obj_level == "2":
        obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
     
        obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)  
     
        if obj_l1 in obj_group and (obj_status == "0" or obj_status == "2"):
          
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="1",user_l1=login_user,updated_at_l1=time_now)
        if obj_l2 in obj_group :
       
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="5",user_l2=login_user,updated_at_l2=time_now)
        
             
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
     
 
    return HttpResponse(u'ok')
 
@login_required()
@permission_verify()
def WorkOrderFlow_deny(request):
#     temp_name = "skworkorders/skworkorders-header.html"
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
    WorkOrderFlow_id = request.GET.get('id', '') 
    login_user = str(request.user) 
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

    return HttpResponse(u'成功')   