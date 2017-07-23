#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log

from .forms import AuditFlow_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime



@login_required()
@permission_verify()
def AuditFlow_index(request):
    temp_name = "skdeploy/skdeploy-header.html"
    allproject = AuditFlow.objects.all()
    return render_to_response('skdeploy/AuditFlow_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def AuditFlow_add(request):
    temp_name = "skdeploy/skdeploy-header.html"
    if request.method == "POST":
        AuditFlow_form = AuditFlow_form(request.POST)
        if AuditFlow_form.is_valid():
            AuditFlow_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdeploy/AuditFlow_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        AuditFlow_form = AuditFlow_form()
        return render_to_response("skdeploy/AuditFlow_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def AuditFlow_del(request):
#    temp_name = "skdeploy/skdeploy-header.html"
    AuditFlow_id = request.GET.get('id', '')
    if AuditFlow_id:
        AuditFlow.objects.filter(id=AuditFlow_id).delete()
    
    if request.method == 'POST':
        AuditFlow_items = request.POST.getlist('AuditFlow_check', [])
        if AuditFlow_items:
            for n in AuditFlow_items:
                AuditFlow.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allproject = AuditFlow.objects.all()
    
 #   return render_to_response("skdeploy/AuditFlow.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
# def AuditFlow_edit(request, ids):
#     obj = AuditFlow.objects.get(id=ids)
#     allproject = AuditFlow.objects.all()
#     return render_to_response("skdeploy/AuditFlow_edit.html", locals(), RequestContext(request))

def AuditFlow_edit(request, ids):
    status = 0
#     asset_types = online_status
    obj = get_object(AuditFlow, id=ids)
#     obj = AuditFlow.objects.get(id=ids)
    if request.method == 'POST':
        obj_f = AuditFlow_form(request.POST, instance=obj)
        if obj_f.is_valid():
            obj_f.save()
            status = 1
        else:
            status = 2
    else:
        obj_f = AuditFlow_form(instance=obj)      
    return render_to_response("skdeploy/AuditFlow_edit.html", locals(), RequestContext(request))




    