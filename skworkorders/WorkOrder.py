#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,Environment,WorkOrderGroup,WorkOrder,WorkOrderFlow
import os,shutil
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log
from lib.file import new_file

from .forms import WorkOrder_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime

from lib.lib_config import get_config_var
from git import Repo

level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)
git_path = get_dir("git_path")
proj_base_dir = get_dir("pro_path")


@login_required()
@permission_verify()
def WorkOrder_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = WorkOrder.objects.filter(template_enable = False)
    
    return render_to_response('skworkorders/WorkOrder_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrder_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_WorkOrder_form = WorkOrder_form(request.POST)
        if tpl_WorkOrder_form.is_valid():
            
            
          
                
            tpl_WorkOrder_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skworkorders/WorkOrder_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_WorkOrder_form = WorkOrder_form()
        return render_to_response("skworkorders/WorkOrder_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def WorkOrder_del(request):
#    temp_name = "skworkorders/skworkorders-header.html"
    WorkOrder_id = request.GET.get('id', '')
    if WorkOrder_id:
        WorkOrder.objects.filter(id=WorkOrder_id).delete()
    
    if request.method == 'POST':
        WorkOrder_items = request.POST.getlist('x_check', [])
        if WorkOrder_items:
            for n in WorkOrder_items:
                WorkOrder.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')

@login_required()
@permission_verify()
def WorkOrder_off(request):
    temp_name = "skworkorders/skworkorders-header.html"
    obj_id = request.GET.get('id', '')
    if obj_id:
        obj = WorkOrder.objects.get(id=obj_id)
        obj.status = "no"
        obj.save()  
    tpl_all = WorkOrder.objects.all()
    return render_to_response('skworkorders/WorkOrder_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrder_on(request):
    temp_name = "skworkorders/skworkorders-header.html"
    obj_id = request.GET.get('id', '')
    if obj_id:
        obj = WorkOrder.objects.get(id=obj_id)
        obj.status = "yes"
        obj.save()  
    tpl_all = WorkOrder.objects.all()
    return render_to_response('skworkorders/WorkOrder_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrder_edit(request):
    temp_name = "skworkorders/skworkorders-header.html"
    ids = request.GET.get('id', '')
    obj = get_object(WorkOrder, id=ids)
    
    
    if request.method == 'POST':
        tpl_WorkOrder_form = WorkOrder_form(request.POST, instance=obj)
        if tpl_WorkOrder_form.is_valid():

            obj_env_id=request.POST.get('env') 
            obj_workorder_name = request.POST.get('name')                  
            obj_env_eng=Environment.objects.get(id=obj_env_id)
         
       
            tpl_WorkOrder_form.save()
           
            ret = []
            message = "SUCCESS\n保存成功" 
            ret.append(message)
            tips = u"保存成功！"
            display_control = ""
            return render_to_response("skworkorders/WorkOrder_edit.html", locals(), RequestContext(request))
        else:
            tips = u"保存失败！"
            display_control = ""
            return render_to_response("skworkorders/WorkOrder_edit.html", locals(), RequestContext(request))
    else:
     
        tpl_WorkOrder_form = WorkOrder_form(instance=obj)      
        display_control = "none"
      
        return render_to_response("skworkorders/WorkOrder_edit.html", locals(), RequestContext(request))



@login_required()
@permission_verify()
def WorkOrder_template(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = WorkOrder.objects.filter(template_enable = True)
    
    return render_to_response('skworkorders/WorkOrder_template.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrder_add_from_template(request,ids):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_WorkOrder_form = WorkOrder_form(request.POST)
        if tpl_WorkOrder_form.is_valid():         
            tpl_WorkOrder_form.save()
            tips = u"提交成功！"
            display_control = ""
        else:
            tips = u"提交失败！"
            display_control = ""
        return render_to_response("skworkorders/WorkOrder_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        obj = get_object(WorkOrder, id=ids)
        print obj.user_dep,
        dic_init={
            'desc':obj.desc,
            'user_dep':obj.user_dep.all(),
            'env':obj.env,
             'group':obj.group,
             'status':obj.status,
              
             'var_built_in':obj.var_built_in,
             'var_opional_switch':obj.var_opional_switch,
             'var_opional':obj.var_opional,
         
             'pre_task':obj.pre_task,
             'main_task':obj.main_task,
             'post_task':obj.post_task,
           
             'audit_enable':obj.audit_enable,
             'audit_flow':obj.audit_flow,
             }
      
        tpl_WorkOrder_form = WorkOrder_form(initial=dic_init) 
        return render_to_response("skworkorders/WorkOrder_add.html", locals(), RequestContext(request))

