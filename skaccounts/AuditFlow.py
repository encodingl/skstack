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
    temp_name = "skaccounts/accounts-header.html"    
    tpl_all = AuditFlow.objects.all()
    
    return render_to_response('skaccounts/AuditFlow_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def AuditFlow_add(request):
    temp_name = "skaccounts/accounts-header.html"
    if request.method == "POST":
        tpl_AuditFlow_form = AuditFlow_form(request.POST)
        if tpl_AuditFlow_form.is_valid():
            tpl_AuditFlow_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skaccounts/AuditFlow_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_AuditFlow_form = AuditFlow_form()
        return render_to_response("skaccounts/AuditFlow_add.html", locals(), RequestContext(request))



@login_required()
@permission_verify()
def AuditFlow_del(request):
#    temp_name = "skaccounts/accounts-header.html"
    AuditFlow_id = request.GET.get('id', '')
    if AuditFlow_id:
        AuditFlow.objects.filter(id=AuditFlow_id).delete()
    
    if request.method == 'POST':
        AuditFlow_items = request.POST.getlist('x_check', [])
        if AuditFlow_items:
            for n in AuditFlow_items:
                AuditFlow.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def AuditFlow_edit(request, ids):
    status = 0
    obj = get_object(AuditFlow, id=ids)
    
    if request.method == 'POST':
        tpl_AuditFlow_form = AuditFlow_form(request.POST, instance=obj)
        if tpl_AuditFlow_form.is_valid():
            tpl_AuditFlow_form.save()
            status = 1
        else:
            status = 2
    else:
        tpl_AuditFlow_form = AuditFlow_form(instance=obj)      
    return render_to_response("skaccounts/AuditFlow_edit.html", locals(), RequestContext(request))
