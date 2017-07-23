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

from .forms import Environment_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime



@login_required()
@permission_verify()
def Environment_index(request):
    temp_name = "skdeploy/skdeploy-header.html"
    allproject = Environment.objects.all()
    return render_to_response('skdeploy/Environment_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def Environment_add(request):
    temp_name = "skdeploy/skdeploy-header.html"
    if request.method == "POST":
        Environment_form = Environment_form(request.POST)
        if Environment_form.is_valid():
            Environment_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdeploy/Environment_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        Environment_form = Environment_form()
        return render_to_response("skdeploy/Environment_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def Environment_del(request):
#    temp_name = "skdeploy/skdeploy-header.html"
    Environment_id = request.GET.get('id', '')
    if Environment_id:
        Environment.objects.filter(id=Environment_id).delete()
    
    if request.method == 'POST':
        Environment_items = request.POST.getlist('Environment_check', [])
        if Environment_items:
            for n in Environment_items:
                Environment.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allproject = Environment.objects.all()
    
 #   return render_to_response("skdeploy/Environment.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
# def Environment_edit(request, ids):
#     obj = Environment.objects.get(id=ids)
#     allproject = Environment.objects.all()
#     return render_to_response("skdeploy/Environment_edit.html", locals(), RequestContext(request))

def Environment_edit(request, ids):
    status = 0
#     asset_types = online_status
    obj = get_object(Environment, id=ids)
#     obj = Environment.objects.get(id=ids)
    if request.method == 'POST':
        obj_f = Environment_form(request.POST, instance=obj)
        if obj_f.is_valid():
            obj_f.save()
            status = 1
        else:
            status = 2
    else:
        obj_f = Environment_form(instance=obj)      
    return render_to_response("skdeploy/Environment_edit.html", locals(), RequestContext(request))




    