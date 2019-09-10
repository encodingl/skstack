#! /usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse
from .models import AuditFlow,Environment,WorkOrder,WorkOrderFlow
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from .forms import WorkOrderCommit_form,WorkOrderCommit_help_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object

from datetime import datetime
import json
from skaccounts.models import UserInfo
from django import forms
from dwebsocket.decorators import accept_websocket

from skworkorders.lib_skworkorders import get_VarsGroup_form,format_to_user_vars,custom_task,permission_submit_pass
from skworkorders.lib_skworkorders2 import PreTask
from lib.lib_json import my_obj_pairs_hook



from datetime import datetime,timedelta
import pytz
from skworkorders import tasks
from skstack.celery import app as celery_app



import logging
log = logging.getLogger('skworkorders')


@login_required()
@permission_verify()
def WorkOrderCommit_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    obj_user = UserInfo.objects.get(username=request.user)
    obj_group = obj_user.usergroup_set.all()

    tpl_env = Environment.objects.all().order_by("name_english")
    tpl_dic_obj={}

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
    return HttpResponse('撤销成功')

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
        if obj.back_exe_enable == False:
            tpl_WorkOrderCommit_form.fields["back_exe_enable"].widget=forms.HiddenInput()
        if obj.auto_exe_enable == False:
            tpl_WorkOrderCommit_form.fields["auto_exe_enable"].widget=forms.HiddenInput()
            
        return render_to_response("skworkorders/WorkOrderCommit_add.html", locals(), RequestContext(request))
    else:
        response_data = {}  
        response_data['result'] = 'failed'  
        response_data['message'] = 'You donot have permisson' 
        return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required()
@permission_verify()
def WorkOrderCommit_help(request, ids):
    temp_name = "skworkorders/skworkorders-header.html"
    obj = get_object(WorkOrder, id=ids)
    obj2 = Environment.objects.get(name_english = obj.env)

    dic_init={'name':obj.name,
              'desc':obj.desc,
              'env':obj2.name_english,
              'audit_enable':obj.audit_enable,
             }
 
    
    tpl_WorkOrderCommit_help_form = WorkOrderCommit_help_form(initial=dic_init)  
   
            
    return render_to_response("skworkorders/WorkOrderCommit_help.html", locals(), RequestContext(request))



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
            pt01 = PreTask(WorkOrder_id,request,message_dic)
            if pt01.permission_submit_pass():
                if pt01.pre_task_success():
                    if pt01.obj.audit_enable == True:
                        if pt01.obj.schedule_enable == True: 
                            pt01.celery_task_create()
                        else:
                            pt01.manual_task_add()
                    else:
                        if  pt01.obj.schedule_enable == True:
                            pt01.celery_task_add()
                        elif pt01.obj.back_exe_enable == True:
                            if "back_exe_enable" in pt01.message_dic_format:
                                pt01.celery_bgtask_add()
                            else:
                                pt01.all_task_do()
                                
                        else:
                            pt01.all_task_do()

                else:
                    pt01.pre_task_failed()
            else:
                pt01.permission_submit_deny()
