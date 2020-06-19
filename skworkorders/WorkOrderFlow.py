#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from .models import AuditFlow,Environment,WorkOrder,WorkOrderFlow

from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify

from .forms import WorkOrderFlow_detail_form,WorkOrderFlow_release_form,CeleryTaskResult_form,Comment_form
from django.shortcuts import render

from lib.com import get_object
from django_celery_results.models import TaskResult
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.core import serializers
from django.forms.models import model_to_dict  


from skaccounts.models import UserInfo,UserGroup
from django.db.models import Q
import json

from dwebsocket.decorators import accept_websocket

from skworkorders.lib_skworkorders2 import WorkOrdkerFlowTask
from skworkorders.lib_skworkorders import dynamic_column_data
import logging


log = logging.getLogger('skworkorders')

@login_required()
@permission_verify()
def WorkOrderFlow_foreground_release(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    current_date=timezone.now()

    tpl_env = Environment.objects.all().order_by("label_sort")
    tpl_dic_obj={}

    for e in tpl_env:
        obj = WorkOrderFlow.objects.filter(celery_schedule_time__isnull=True,auto_exe_enable=False,user_commit=request.user,env=e.name_english,created_at__range=(current_date + timedelta(days=-7),current_date),celery_task_id__isnull=True)
        tpl_dic_obj[e.name_english]=obj

    return render(request,'skworkorders/WorkOrderFlow_foreground_release.html', locals())


@login_required()
@permission_verify()
def WorkOrderFlow_background_release(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    current_date=timezone.now()
    from_date = current_date + timedelta(days=-7)
    

    tpl_env = Environment.objects.all().order_by("label_sort")
    tpl_dic_obj={}
    
    for e in tpl_env:

        obj = WorkOrderFlow.objects.raw("select a.id,a.title,a.status,b.status as b_status from skworkorders_workorderflow as a \
                                            LEFT JOIN django_celery_results_taskresult as b ON a.celery_task_id = b.task_id \
                                            where a.created_at between %s and %s and a.user_commit=%s and a.env=%s and \
                                            (a.celery_task_id is not NUll or a.auto_exe_enable=True or a.celery_schedule_time is not NUll)",\
                                            params=[from_date,current_date,request.user,e.name_english]) 
        tpl_dic_obj[e.name_english]=obj
        

    tpl_today = datetime.now()
    return render(request,'skworkorders/WorkOrderFlow_background_release.html', locals())



@login_required()
@permission_verify()
def WorkOrderFlow_foreground_history(request):
    temp_name = "skworkorders/skworkorders-header.html"  
    current_date=timezone.now()  
    tpl_env = Environment.objects.all().order_by("label_sort")
    tpl_dic_obj={}
    if request.method == 'POST':
        from_date = request.POST.get('from_date', '')
        print(from_date)
        print(type(from_date))
        from_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
       
        to_date = request.POST.get('to_date', '')
        to_date = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")

        for e in tpl_env:
            obj = WorkOrderFlow.objects.filter(env=e.name_english,created_at__range=(from_date,to_date),celery_task_id__isnull=True)
            tpl_dic_obj[e.name_english]=obj
    else:
    

        for e in tpl_env:
            obj = WorkOrderFlow.objects.filter(env=e.name_english,created_at__range=(current_date + timedelta(days=-30),current_date),celery_task_id__isnull=True)
            tpl_dic_obj[e.name_english]=obj
    

    
    return render(request,'skworkorders/WorkOrderFlow_foreground_history.html', locals())
 
@login_required()
@permission_verify()
def WorkOrderFlow_background_history(request):
    temp_name = "skworkorders/skworkorders-header.html"  
    current_date=timezone.now()  
    from_date = current_date + timedelta(days=-30)
    tpl_env = Environment.objects.all().order_by("label_sort")
    tpl_dic_obj={}
    if request.method == 'POST':
        from_date = request.POST.get('from_date', '')
        from_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        to_date = request.POST.get('to_date', '')
        to_date = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
        

        for e in tpl_env:
            #obj = WorkOrderFlow.objects.filter(env=e.name_english,created_at__range=(from_date,to_date),celery_task_id__isnull=False)
            obj = WorkOrderFlow.objects.raw("select a.id,a.title,a.status,b.status as b_status from skworkorders_workorderflow as a \
                                            LEFT JOIN django_celery_results_taskresult as b ON a.celery_task_id = b.task_id \
                                            where a.created_at between %s and %s and a.env=%s and \
                                            (a.celery_task_id is not NUll or a.auto_exe_enable=True)",\
                                            params=[from_date,to_date,e.name_english])
            tpl_dic_obj[e.name_english]=obj
    else:

        
        
     
    
        for e in tpl_env:
            obj = WorkOrderFlow.objects.raw("select a.id,a.title,a.status,b.status as b_status from skworkorders_workorderflow as a \
                                            LEFT JOIN django_celery_results_taskresult as b ON a.celery_task_id = b.task_id \
                                            where a.created_at between %s and %s and a.env=%s and \
                                            (a.celery_task_id is not NUll or a.auto_exe_enable=True)",\
                                            params=[from_date,current_date,e.name_english])
           
            tpl_dic_obj[e.name_english]=obj
    

    tpl_today = datetime.now()
    return render(request,'skworkorders/WorkOrderFlow_background_history.html', locals())
 
@login_required()
@permission_verify()
def WorkOrderFlow_revoke(request):
#     temp_name = "skworkorders/skworkorders-header.html"
    
    login_user = request.user
    WorkOrderFlow_id = request.GET.get('id', '')
    t01 =  WorkOrdkerFlowTask(WorkOrderFlow_id,login_user,request)
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if WorkOrderFlow_id:
        if t01.obj.celery_task_id:
            t01.celery_task_revoke()
        else:
            WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="9",finished_at=time_now)
        return HttpResponse('successful')
    else:
        return HttpResponse('the WorkOrderFlow_id didnot exist')
        
  

               
    
 
 
 
@login_required()
@permission_verify()
def WorkOrderFlow_foreground_detail(request,ids):
    obj = get_object(WorkOrderFlow, id=ids)
    tpl_WorkOrderFlow_form = WorkOrderFlow_detail_form(instance=obj) 
    return render(request,"skworkorders/WorkOrderFlow_foreground_detail.html", locals())
 
@login_required()
@permission_verify()
def WorkOrderFlow_background_detail(request): 
    task_id = request.GET.get('task_id', '')  
    obj = get_object(TaskResult, task_id=task_id) 
    obj2 = get_object(WorkOrderFlow, celery_task_id=task_id)
    
    
    
    if not obj:
        if  obj2:
            if obj2.back_exe_enable == True:
                tpl_celery_task_status = "任务已结束，任务队列结果已清理，执行结果日志请查看celery日志"
            elif obj2.auto_exe_enable == True:
                tpl_celery_task_status = "任务已结束，任务队列结果已清理，执行结果日志请查看celery日志"
            elif obj2.status == "CREATED" or obj2.status == "PENDING"  :
                celery_schedule_time = obj2.celery_schedule_time
                time_now = datetime.now()
                if time_now > celery_schedule_time:
                    tpl_celery_task_status = "任务已结束，任务队列结果已清理，执行结果日志请查看celery日志"
                else:
                    tpl_celery_task_status = "任务未开始，请等待计划时间执行后再查看"
            elif obj2.status == "9":
                tpl_celery_task_status = "任务已撤销，无执行详情信息"
        else:
            tpl_celery_task_status = "任务未开始,等待审批后自动执行"
            
    else:
        obj=obj.as_dict()
        tpl_CeleryTaskResult_form = CeleryTaskResult_form(initial=obj)
        
    if  obj2:
            tpl_WorkOrderFlow_form = WorkOrderFlow_detail_form(instance=obj2)    
    return render(request,"skworkorders/WorkOrderFlow_background_detail.html", locals())
 
@login_required()
@permission_verify()
def WorkOrderFlow_release(request, ids):
    temp_name = "skworkorders/skworkorders-header.html"
    obj = get_object(WorkOrderFlow, id=ids) 
    obj_title=obj.title
    dic_init={'workorder':obj.workorder,
                 'env':obj.env,
                 'user_vars':obj.user_vars,            
                 }
    tpl_WorkOrderFlow_release_form = WorkOrderFlow_release_form(initial=dic_init)  
    return render(request,"skworkorders/WorkOrderFlow_release.html", locals())
 
 
 
  
     
     
 
@accept_websocket
@login_required()
@permission_verify()
def WorkOrderFlow_release_run(request):
    temp_name = "skworkorders/skworkorders-header.html" 
    if not request.is_websocket():#判断是不是websocket连接
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request,'skworkorders/websocket.html', locals())
    else:
        for message in request.websocket:
            WorkOrderFlow_id = int(message)   
            user = request.user
            t01=WorkOrdkerFlowTask(WorkOrderFlow_id,user,request)
            content_str = "execute starting"
            t01.log("info", content_str)
            if t01.permission_audit_pass():
                if t01.permission_submit_pass():
                    if t01.obj.celery_task_id:
                        t01.celery_task_changeto_manual_task()
                    t01.all_task_do()
                   
                else:
                    t01.permission_submit_deny()
            else:
                t01.permission_audit_deny()
                

 
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
   

    
    tpl_env = Environment.objects.all().order_by("label_sort")
    tpl_dic_obj={}

    for e in tpl_env:
        obj = WorkOrderFlow.objects.filter(workorder_id__in=obj_workorder,env=e.name_english,created_at__range=(current_date + timedelta(days=-30),current_date)).exclude(status__in=[3,4,9,"CREATED","PENDING"])
        tpl_dic_obj[e.name_english]=obj
    tpl_today = datetime.now()
    return render(request,'skworkorders/WorkOrderFlow_audit.html', locals())
 
@login_required()
@permission_verify()
def WorkOrderFlow_permit(request):

    if request.method == "POST":
        tpl_Comment_form = Comment_form(request.POST)
        if tpl_Comment_form.is_valid():
            comment_content = request.POST["comment_content"]
            WorkOrderFlow_id = request.POST["id"]

            

            login_user = request.user  
            login_user = str(login_user) 
            obj_user = UserInfo.objects.get(username=request.user)    
            obj_group = obj_user.usergroup_set.all()   
            obj_WorkOrderFlow = WorkOrderFlow.objects.get(id=WorkOrderFlow_id)
            obj_WorkOrder = WorkOrder.objects.get(id=obj_WorkOrderFlow.workorder_id)
            obj_AuditFlow = AuditFlow.objects.get(name = obj_WorkOrder.audit_flow)   
            obj_level = obj_AuditFlow.level
            obj_status = obj_WorkOrderFlow.status
            t01 = WorkOrdkerFlowTask(WorkOrderFlow_id,login_user,request)
            time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            if obj_level == "1":
                obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
                if obj_l1 in obj_group:
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="1",user_l1=login_user,comment_l1=comment_content,updated_at_l1=time_now)
                    if t01.obj.celery_schedule_time:
                        t01.celery_task_add()
                    elif t01.obj.auto_exe_enable:
                        t01.celery_task_add()
                  
            elif obj_level == "2":
                obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
                obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)  
                if obj_l1 in obj_group and (obj_status == "0" or obj_status == "2"):
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="1",user_l1=login_user,comment_l1=comment_content,updated_at_l1=time_now)
                if obj_l2 in obj_group :     
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="5",user_l2=login_user,comment_l2=comment_content,updated_at_l2=time_now)
                    if t01.obj.celery_schedule_time:
                        t01.celery_task_add()
                    elif t01.obj.auto_exe_enable:
                        t01.celery_task_add()
        
            elif obj_level == "3" and (obj_status == "0" or obj_status == "2" or obj_status == "6" or obj_status == "8"): 
                obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
                obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)
                obj_l3 = UserGroup.objects.get(name=obj_AuditFlow.l3)  
                if obj_l1 in obj_group and (obj_status == "0" or obj_status == "2"):
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="1",comment_l1=comment_content,user_l1=login_user,updated_at_l1=time_now)
                if obj_l2 in obj_group and (obj_status == "0" or obj_status == "2" or obj_status == "1" or obj_status == "6"):
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="5",user_l2=login_user,comment_l2=comment_content,updated_at_l2=time_now)
                if obj_l3 in obj_group :
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="7",user_l3=login_user,comment_l3=comment_content,updated_at_l3=time_now)
                    if t01.obj.celery_schedule_time:
                        t01.celery_task_add()
                    elif t01.obj.auto_exe_enable:
                        t01.celery_task_add()
            status = 1
        else:
            status = 2
    else:
        tpl_Comment_form = Comment_form()
        tpl_id = request.GET.get('id', '')
    return render(request,'skworkorders/WorkOrderFlow_permit.html', locals())

    
    
     
 
    return HttpResponse('ok')
 
@login_required()
@permission_verify()
def WorkOrderFlow_deny(request):
    if request.method == "POST":
        tpl_Comment_form = Comment_form(request.POST)
        if tpl_Comment_form.is_valid():
            comment_content = request.POST["comment_content"]
            WorkOrderFlow_id = request.POST["id"]
            
            
            time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')   
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
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="2",user_l1=login_user,comment_l1=comment_content,updated_at_l1=time_now)
                     
            elif obj_level == "2":
                obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
                obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)   
                if obj_l1 in obj_group and (obj_status == "0" or obj_status == "1"):
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="2",user_l1=login_user,comment_l1=comment_content,updated_at_l1=time_now)
                if obj_l2 in obj_group:
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="6",user_l2=login_user,comment_l2=comment_content,updated_at_l2=time_now)
                     
            elif obj_level == "3": 
                obj_l1 = UserGroup.objects.get(name=obj_AuditFlow.l1)
                obj_l2 = UserGroup.objects.get(name=obj_AuditFlow.l2)
                obj_l3 = UserGroup.objects.get(name=obj_AuditFlow.l3)  
                if obj_l1 in obj_group and (obj_status == "0" or obj_status == "1"):
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="2",user_l1=login_user,comment_l1=comment_content,updated_at_l1=time_now)
                if obj_l2 in obj_group and (obj_status == "0" or obj_status == "2" or obj_status == "1" or obj_status == "5"):
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="6",user_l2=login_user,comment_l2=comment_content,updated_at_l2=time_now)
                if obj_l3 in obj_group:
                    WorkOrderFlow.objects.filter(id=WorkOrderFlow_id).update(status="8",user_l3=login_user,comment_l3=comment_content,updated_at_l3=time_now)
            status = 1
        else:
            status = 2
    else:
        tpl_Comment_form = Comment_form()
        tpl_id = request.GET.get('id', '')
    return render(request,'skworkorders/WorkOrderFlow_deny.html', locals())
    