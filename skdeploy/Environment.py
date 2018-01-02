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


git_path = get_dir("git_path")
level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)
proj_base_dir = get_dir("pro_path")

@login_required()
@permission_verify()
def Environment_index(request):
    temp_name = "skdeploy/skdeploy-header.html"    
    tpl_all = Environment.objects.all()
    
    return render_to_response('skdeploy/Environment_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def Environment_add(request):
    temp_name = "skdeploy/skdeploy-header.html"
    if request.method == "POST":
        tpl_Environment_form = Environment_form(request.POST)
        if tpl_Environment_form.is_valid():
            env_git_dir=git_path+request.POST.get('name_english')
            env_proj_dir=proj_base_dir+request.POST.get('name_english')
            try:
                
                os.makedirs(env_git_dir)
                os.makedirs(env_proj_dir)
            except:
                exinfo=sys.exc_info()
                logging.error(exinfo)
                
            tpl_Environment_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdeploy/Environment_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_Environment_form = Environment_form()
        return render_to_response("skdeploy/Environment_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def Environment_del(request):
#    temp_name = "skdeploy/skdeploy-header.html"
    Environment_id = request.GET.get('id', '')
    if Environment_id:
        Environment.objects.filter(id=Environment_id).delete()
    
    if request.method == 'POST':
        Environment_items = request.POST.getlist('x_check', [])
        if Environment_items:
            for n in Environment_items:
                Environment.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allproject = Environment.objects.all()
    
 #   return render_to_response("skdeploy/Environment.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def Environment_edit(request, ids):
    status = 0
    obj = get_object(Environment, id=ids)
    
    if request.method == 'POST':
        tpl_Environment_form = Environment_form(request.POST, instance=obj)
        if tpl_Environment_form.is_valid():
            env_git_dir=git_path+request.POST.get('name_english')
            env_proj_dir=proj_base_dir+request.POST.get('name_english')
            print env_proj_dir
            try:
                
                os.mkdir(env_git_dir)
                
            except:
                exinfo=sys.exc_info()
                logging.error(exinfo)
            try:
                os.mkdir(env_proj_dir)
            except:
                exinfo=sys.exc_info()
                logging.error(exinfo)
        
            tpl_Environment_form.save()
            status = 1
        else:
            status = 2
    else:
        tpl_Environment_form = Environment_form(instance=obj)      
    return render_to_response("skdeploy/Environment_edit.html", locals(), RequestContext(request))




    