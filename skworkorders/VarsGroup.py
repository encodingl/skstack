#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,Environment,VarsGroup,WorkOrder,WorkOrderFlow,Vars,VarsGroup
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log

from .forms import VarsGroup_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime



@login_required()
@permission_verify()
def VarsGroup_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = VarsGroup.objects.all()
    print tpl_all
    return render_to_response('skworkorders/VarsGroup_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def VarsGroup_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_VarsGroup_form = VarsGroup_form(request.POST)
        if tpl_VarsGroup_form.is_valid():
            tpl_VarsGroup_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skworkorders/VarsGroup_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_VarsGroup_form = VarsGroup_form()
        return render_to_response("skworkorders/VarsGroup_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def VarsGroup_del(request):
#    temp_name = "skworkorders/skworkorders-header.html"
    VarsGroup_id = request.GET.get('id', '')
    if VarsGroup_id:
        VarsGroup.objects.filter(id=VarsGroup_id).delete()
    
    if request.method == 'POST':
        VarsGroup_items = request.POST.getlist('x_check', [])
        if VarsGroup_items:
            for n in VarsGroup_items:
                VarsGroup.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allworkorder = VarsGroup.objects.all()
    
 #   return render_to_response("skworkorders/VarsGroup.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def VarsGroup_edit(request, ids):
    temp_name = "skworkorders/skworkorders-header.html"
    obj = get_object(VarsGroup, id=ids)
    
    if request.method == 'POST':
        tpl_VarsGroup_form = VarsGroup_form(request.POST, instance=obj)
        if tpl_VarsGroup_form.is_valid():
            tpl_VarsGroup_form.save()
            tips = u"保存成功！"
            display_control = ""
        else:
            tips = u"保存失败！"
            display_control = ""
    else:
        display_control = "none"
        tpl_VarsGroup_form = VarsGroup_form(instance=obj)      
    return render_to_response("skworkorders/VarsGroup_edit.html", locals(), RequestContext(request))
