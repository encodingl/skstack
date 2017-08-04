#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,Project,ProjectGroup,Project,TaskStatus,Environment
import os,shutil
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log
from lib.file import new_file
from gittle import Gittle
from .forms import Project_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime


level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)
git_path = get_dir("git_path")
proj_base_dir = get_dir("pro_path")


@login_required()
@permission_verify()
def Project_index(request):
    temp_name = "skdeploy/skdeploy-header.html"    
    tpl_all = Project.objects.all()
    
    return render_to_response('skdeploy/Project_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def Project_add(request):
    temp_name = "skdeploy/skdeploy-header.html"
    if request.method == "POST":
        tpl_Project_form = Project_form(request.POST)
        if tpl_Project_form.is_valid():
            obj_env_id=request.POST.get('env') 
            obj_project_name = request.POST.get('name')                  
            obj_env_eng=Environment.objects.get(id=obj_env_id)
            
            repo_path = git_path+obj_env_eng.name_english+"/"+obj_project_name
            
            try:
              
                repo_url = request.POST.get('repo_url')
                repo = Gittle.clone(repo_url, repo_path)

            except:
                exinfo=sys.exc_info()
                logging.error(exinfo)
                
            tpl_Project_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdeploy/Project_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_Project_form = Project_form()
        return render_to_response("skdeploy/Project_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def Project_del(request):
#    temp_name = "skdeploy/skdeploy-header.html"
    Project_id = request.GET.get('id', '')
    if Project_id:
        Project.objects.filter(id=Project_id).delete()
    
    if request.method == 'POST':
        Project_items = request.POST.getlist('x_check', [])
        if Project_items:
            for n in Project_items:
                Project.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allproject = Project.objects.all()
    
 #   return render_to_response("skdeploy/Project.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def Project_edit(request, ids):
    status = 0
    obj = get_object(Project, id=ids)
    
    if request.method == 'POST':
        tpl_Project_form = Project_form(request.POST, instance=obj)
        if tpl_Project_form.is_valid():

            obj_env_id=request.POST.get('env') 
            obj_project_name = request.POST.get('name')                  
            obj_env_eng=Environment.objects.get(id=obj_env_id)
             
            
            repo_path = git_path+obj_env_eng.name_english+"/"+obj_project_name
            proj_dir = proj_base_dir+obj_env_eng.name_english+"/"+obj_project_name
            print proj_dir
        
            try:
                if os.path.exists(repo_path):
                    shutil.rmtree(repo_path)
               
                repo_url = request.POST.get('repo_url')
                repo = Gittle.clone(repo_url, repo_path)
                if os.path.exists(proj_dir):
                    shutil.rmtree(proj_dir)
                os.mkdir(proj_dir)
                os.chdir(proj_dir)
                new_file("pre_deploy.sh", obj.pre_deploy)
                new_file("post_deploy.sh", obj.post_deploy)
                new_file("pre_release.sh", obj.post_deploy)
                new_file("post_release.sh", obj.post_deploy)
               
            

            except:
                exinfo=sys.exc_info()
                logging.error(exinfo)
                
            
            
         
                
            tpl_Project_form.save()
            status = 1
        else:
            status = 2
    else:
        tpl_Project_form = Project_form(instance=obj)      
    return render_to_response("skdeploy/Project_edit.html", locals(), RequestContext(request))
