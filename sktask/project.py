#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import project,job,extravars
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify,permission_verify_ids
import logging
from lib.log import log
from lib.setup import get_playbook, get_roles, get_AnsibleHostsDic
from .models import history
from .forms import Project_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from .models import history
from datetime import datetime

# var info

proj_base_dir = get_dir("pro_path")
ansible_dir = get_dir("a_path")





@login_required()
@permission_verify()
def project_manage(request, *args, **kwargs):
    temp_name = "sktask/setup-header.html"
    allproject = project.objects.all()
    return render_to_response('sktask/project_manage.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def project_add(request, *args, **kwargs):
    temp_name = "sktask/setup-header.html"
    if request.method == "POST":
        project_form = Project_form(request.POST)
        if project_form.is_valid():
            project_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("sktask/project_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        project_form = Project_form()
        return render_to_response("sktask/project_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def project_del(request, *args, **kwargs):
#    temp_name = "sktask/setup-header.html"
    project_id = request.GET.get('id', '')
    if project_id:
        project.objects.filter(id=project_id).delete()
    
    if request.method == 'POST':
        project_items = request.POST.getlist('project_check', [])
        if project_items:
            for n in project_items:
                project.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allproject = project.objects.all()
    
 #   return render_to_response("sktask/project.html", locals(), RequestContext(request))


@login_required()
@permission_verify_ids()
# def project_edit(request, ids):
#     obj = project.objects.get(id=ids)
#     allproject = project.objects.all()
#     return render_to_response("sktask/project_edit.html", locals(), RequestContext(request))

def project_edit(request, ids):
    status = 0
#     asset_types = online_status
    obj = get_object(project, id=ids)
#     obj = project.objects.get(id=ids)
    if request.method == 'POST':
        obj_f = Project_form(request.POST, instance=obj)
        if obj_f.is_valid():
            obj_f.save()
            status = 1
        else:
            status = 2
    else:
        obj_f = Project_form(instance=obj)      
    return render_to_response("sktask/project_edit.html", locals(), RequestContext(request))




    