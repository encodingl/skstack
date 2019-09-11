#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .models import ConfigCenter
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from .forms import ConfigCenter_form
from django.shortcuts import render_to_response
from django.template import RequestContext
from skcmdb.api import get_object
import logging
from lib.lib_fabric import  ssh_cmd_back
log = logging.getLogger('skworkorders')


@login_required()
@permission_verify()
def ConfigCenter_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = ConfigCenter.objects.all()
    
    return render_to_response('skworkorders/ConfigCenter_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def ConfigCenter_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_ConfigCenter_form = ConfigCenter_form(request.POST)
        if tpl_ConfigCenter_form.is_valid():     
            tpl_ConfigCenter_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render_to_response("skworkorders/ConfigCenter_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_ConfigCenter_form = ConfigCenter_form()
        return render_to_response("skworkorders/ConfigCenter_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def ConfigCenter_del(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    obj_id = request.GET.get('id', '')  
    if obj_id:
        try:
            ConfigCenter.objects.filter(id=obj_id).delete()
        except Exception as tpl_error_msg:
            log.warning(tpl_error_msg)
        tpl_all = ConfigCenter.objects.all()
        return render_to_response("skworkorders/ConfigCenter_index.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def ConfigCenter_edit(request, ids):
    status = 0
    obj = get_object(ConfigCenter, id=ids)
    
    if request.method == 'POST':
        tpl_ConfigCenter_form = ConfigCenter_form(request.POST, instance=obj)
        if tpl_ConfigCenter_form.is_valid():

            tpl_ConfigCenter_form.save()
            status = 1
        else:
            status = 2
    else:
        tpl_ConfigCenter_form = ConfigCenter_form(instance=obj)      
    return render_to_response("skworkorders/ConfigCenter_edit.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def ConfigCenter_check(request,ids):
    temp_name = "skworkorders/skworkorders-header.html"
    obj = get_object(ConfigCenter, id=ids)
    cmd = "date"
    ret,retcode = ssh_cmd_back(obj.ip,obj.port,obj.username,obj.password,cmd,obj.rsa_key)
    ret.insert(0,"SSH登陆验证:检测配置中心时间")
    if retcode == 0:
        ret.append("执行成功")
    else:
        ret.append("执行失败")
    return render_to_response("skworkorders/ConfigCenter_check.html", locals(), RequestContext(request))


    