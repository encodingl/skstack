#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,ProjectGroup,Project,ProjectGroup,TaskStatus
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify,permission_verify_ids
import logging
from lib.log import log

from .forms import ProjectGroup_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime



@login_required()
@permission_verify()
def ProjectGroup_index(request, *args, **kwargs):
    temp_name = "skdeploy/skdeploy-header.html"    
    tpl_all = ProjectGroup.objects.all()
    print tpl_all
    return render_to_response('skdeploy/ProjectGroup_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def ProjectGroup_add(request, *args, **kwargs):
    temp_name = "skdeploy/skdeploy-header.html"
    if request.method == "POST":
        tpl_ProjectGroup_form = ProjectGroup_form(request.POST)
        if tpl_ProjectGroup_form.is_valid():
            tpl_ProjectGroup_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdeploy/ProjectGroup_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_ProjectGroup_form = ProjectGroup_form()
        return render_to_response("skdeploy/ProjectGroup_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def ProjectGroup_del(request, *args, **kwargs):
#    temp_name = "skdeploy/skdeploy-header.html"
    ProjectGroup_id = request.GET.get('id', '')
    if ProjectGroup_id:
        ProjectGroup.objects.filter(id=ProjectGroup_id).delete()
    
    if request.method == 'POST':
        ProjectGroup_items = request.POST.getlist('x_check', [])
        if ProjectGroup_items:
            for n in ProjectGroup_items:
                ProjectGroup.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allproject = ProjectGroup.objects.all()
    
 #   return render_to_response("skdeploy/ProjectGroup.html", locals(), RequestContext(request))


@login_required()
@permission_verify_ids()
def ProjectGroup_edit(request, ids):
    status = 0
    obj = get_object(ProjectGroup, id=ids)
    
    if request.method == 'POST':
        tpl_ProjectGroup_form = ProjectGroup_form(request.POST, instance=obj)
        if tpl_ProjectGroup_form.is_valid():
            tpl_ProjectGroup_form.save()
            status = 1
        else:
            status = 2
    else:
        tpl_ProjectGroup_form = ProjectGroup_form(instance=obj)      
    return render_to_response("skdeploy/ProjectGroup_edit.html", locals(), RequestContext(request))
