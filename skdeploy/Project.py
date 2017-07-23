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

from .forms import Project_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime



@login_required()
@permission_verify()
def Project_index(request):
    temp_name = "skdeploy/skdeploy-header.html"
    allproject = Project.objects.all()
    return render_to_response('skdeploy/Project_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def Project_add(request):
    temp_name = "skdeploy/skdeploy-header.html"
    if request.method == "POST":
        Project_form = Project_form(request.POST)
        if Project_form.is_valid():
            Project_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdeploy/Project_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        Project_form = Project_form()
        return render_to_response("skdeploy/Project_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def Project_del(request):
#    temp_name = "skdeploy/skdeploy-header.html"
    Project_id = request.GET.get('id', '')
    if Project_id:
        Project.objects.filter(id=Project_id).delete()
    
    if request.method == 'POST':
        Project_items = request.POST.getlist('Project_check', [])
        if Project_items:
            for n in Project_items:
                Project.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allproject = Project.objects.all()
    
 #   return render_to_response("skdeploy/Project.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
# def Project_edit(request, ids):
#     obj = Project.objects.get(id=ids)
#     allproject = Project.objects.all()
#     return render_to_response("skdeploy/Project_edit.html", locals(), RequestContext(request))

def Project_edit(request, ids):
    status = 0
#     asset_types = online_status
    obj = get_object(Project, id=ids)
#     obj = Project.objects.get(id=ids)
    if request.method == 'POST':
        obj_f = Project_form(request.POST, instance=obj)
        if obj_f.is_valid():
            obj_f.save()
            status = 1
        else:
            status = 2
    else:
        obj_f = Project_form(instance=obj)      
    return render_to_response("skdeploy/Project_edit.html", locals(), RequestContext(request))




    