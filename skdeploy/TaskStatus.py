#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,Environment,ProjectGroup,Project,TaskStatus
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log

from .forms import TaskStatus_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime



@login_required()
@permission_verify()
def TaskStatus_index(request):
    temp_name = "skdeploy/skdeploy-header.html"
    allproject = TaskStatus.objects.all()
    return render_to_response('skdeploy/TaskStatus_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def TaskStatus_add(request):
    temp_name = "skdeploy/skdeploy-header.html"
    if request.method == "POST":
        TaskStatus_form = TaskStatus_form(request.POST)
        if TaskStatus_form.is_valid():
            TaskStatus_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdeploy/TaskStatus_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        TaskStatus_form = TaskStatus_form()
        return render_to_response("skdeploy/TaskStatus_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def TaskStatus_del(request):
#    temp_name = "skdeploy/skdeploy-header.html"
    TaskStatus_id = request.GET.get('id', '')
    if TaskStatus_id:
        TaskStatus.objects.filter(id=TaskStatus_id).delete()
    
    if request.method == 'POST':
        TaskStatus_items = request.POST.getlist('TaskStatus_check', [])
        if TaskStatus_items:
            for n in TaskStatus_items:
                TaskStatus.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allproject = TaskStatus.objects.all()
    
 #   return render_to_response("skdeploy/TaskStatus.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
# def TaskStatus_edit(request, ids):
#     obj = TaskStatus.objects.get(id=ids)
#     allproject = TaskStatus.objects.all()
#     return render_to_response("skdeploy/TaskStatus_edit.html", locals(), RequestContext(request))

def TaskStatus_edit(request, ids):
    status = 0
#     asset_types = online_status
    obj = get_object(TaskStatus, id=ids)
#     obj = TaskStatus.objects.get(id=ids)
    if request.method == 'POST':
        obj_f = TaskStatus_form(request.POST, instance=obj)
        if obj_f.is_valid():
            obj_f.save()
            status = 1
        else:
            status = 2
    else:
        obj_f = TaskStatus_form(instance=obj)      
    return render_to_response("skdeploy/TaskStatus_edit.html", locals(), RequestContext(request))




    