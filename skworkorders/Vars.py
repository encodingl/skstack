#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,Environment,Vars,WorkOrder,WorkOrderFlow,Vars,VarsGroup
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log

from .forms import Vars_form,Vars_Select_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime
from lib.lib_format import list_to_formlist
import commands
import time



@login_required()
@permission_verify()
def Vars_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = Vars.objects.all()
    
    return render_to_response('skworkorders/Vars_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def Vars_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_Vars_form = Vars_form(request.POST)
        if tpl_Vars_form.is_valid():
            tpl_Vars_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skworkorders/Vars_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_Vars_form = Vars_form()
        return render_to_response("skworkorders/Vars_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def Vars_del(request):
#    temp_name = "skworkorders/skworkorders-header.html"
    Vars_id = request.GET.get('id', '')
    if Vars_id:
        Vars.objects.filter(id=Vars_id).delete()
    
    if request.method == 'POST':
        Vars_items = request.POST.getlist('x_check', [])
        if Vars_items:
            for n in Vars_items:
                Vars.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')

@login_required()
@permission_verify()
def Vars_copy(request):
    temp_name = "skworkorders/skworkorders-header.html"
    Vars_id = request.GET.get('id', '')
    if Vars_id:
        obj = Vars.objects.get(id=Vars_id)
        obj.pk=None
        obj.name = obj.name + "_copy_" + time.strftime("%H%M%S", time.localtime()) 
        obj.save()  
    tpl_all = Vars.objects.all()
    return render_to_response('skworkorders/Vars_index.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def Vars_edit(request, ids):
    status = 0
    obj = get_object(Vars, id=ids)
    
    if request.method == 'POST':
        tpl_Vars_form = Vars_form(request.POST, instance=obj)
        if tpl_Vars_form.is_valid():
            tpl_Vars_form.save()
            status = 1
        else:
            status = 2
    else:
        tpl_Vars_form = Vars_form(instance=obj)      
    return render_to_response("skworkorders/Vars_edit.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def Vars_check(request,ids):
    temp_name = "skworkorders/skworkorders-header.html"


    obj = get_object(Vars, id=ids)
    
#判断表单格式生成合适表单    
    if obj.value_form_type == "Select":
        tpl_var_check_form = Vars_Select_form()
    elif obj.value_form_type == "SelectMultiple":
        pass
    elif obj.value_form_type == "TextInput":
        pass
    elif obj.value_form_type == "Textarea":
        pass
    else:
        pass
    
#判断变量来源获取变量内容    
    if obj.value_method == "admin_def":
        obj_value_optional = eval(obj.value_optional)
        tpl_var_check_form.fields["value_optional"].widget.choices = list_to_formlist(obj_value_optional)
    elif obj.value_method == "script":
        obj_value_optional = eval(commands.getoutput(obj.value_script))
        tpl_var_check_form.fields["value_optional"].widget.choices = list_to_formlist(obj_value_optional)
    elif obj.value_method == "manual":
        pass

    return render_to_response("skworkorders/Vars_check.html", locals(), RequestContext(request))
