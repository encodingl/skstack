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

from .forms import Project_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime
from lib.lib_skdeploy import create_release_path,var_change
from lib.lib_config import get_config_var
from git import Repo

level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)
git_path = get_dir("git_path")
proj_base_dir = get_dir("pro_path")


@login_required()
@permission_verify()
def Project_index(request):
    temp_name = "skdeploy/skdeploy-header.html"    
    tpl_all = Project.objects.filter(template_enable = False)
    
    return render_to_response('skdeploy/Project_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def Project_add(request):
    temp_name = "skdeploy/skdeploy-header.html"
    if request.method == "POST":
        tpl_Project_form = Project_form(request.POST)
        if tpl_Project_form.is_valid():
            
            
          
                
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
    temp_name = "skdeploy/skdeploy-header.html"
    
    obj = get_object(Project, id=ids)
    
    if request.method == 'POST':
        tpl_Project_form = Project_form(request.POST, instance=obj)
        if tpl_Project_form.is_valid():

            obj_env_id=request.POST.get('env') 
            obj_project_name = request.POST.get('name')                  
            obj_env_eng=Environment.objects.get(id=obj_env_id)
            if obj.release_library.endswith('/'):
                obj_release_dir = obj.release_library + obj.name
            else:
                obj_release_dir = obj.release_library + "/" + obj.name      
        
            repo_path = git_path+obj_env_eng.name_english+"/"+obj_project_name
            proj_dir = proj_base_dir+obj_env_eng.name_english+"/"+obj_project_name
       
            tpl_Project_form.save()
           
            ret = []
            message = "SUCCESS\n保存成功" 
            ret.append(message)
            tips = u"保存成功！"
            display_control = ""
            return render_to_response("skdeploy/Project_edit.html", locals(), RequestContext(request))
        else:
            tips = u"保存失败！"
            display_control = ""
            return render_to_response("skdeploy/Project_edit.html", locals(), RequestContext(request))
    else:
        tpl_Project_form = Project_form(instance=obj)      
        display_control = "none"
        return render_to_response("skdeploy/Project_edit.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def Project_init(request):
    temp_name = "skdeploy/skdeploy-header.html"

    Project_id = request.GET.get('id')
    obj = get_object(Project, id=Project_id)
    obj_env = str(obj.env)
    obj_project = obj.name
    obj_type = obj.repo_type
    pre_release_base_path = get_config_var("release_path")
    pre_release_proj_path = pre_release_base_path+obj_env+"/"+obj_project+"/"
    
    proj_dir = proj_base_dir+obj_env+"/"+obj_project
    ret = []
    if obj.release_library.endswith('/'):
        obj_release_dir = obj.release_library + obj.name
    else:
        obj_release_dir = obj.release_library + "/" + obj.name 
        
    if obj_type == "git":
        repo_path = git_path+obj_env+"/"+obj_project

        try:
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            repo_url = obj.repo_url
#             repo = Gittle.clone(repo_url, repo_path)
            Repo.clone_from(url=repo_url, to_path=repo_path)

        except:
            exinfo=sys.exc_info()
            logging.error(exinfo)
            ret.append(exinfo)
        
    
    try:
        if os.path.exists(proj_dir):
                shutil.rmtree(proj_dir)        
        os.mkdir(proj_dir)
        os.chdir(proj_dir)
        dic_project={
             'repo_path':repo_path,
             'pre_release_path':pre_release_proj_path,
             'env':obj_env,
             'project':obj_project,
             'repo_url':repo_url,
             'release_user':obj.release_user,                
             'release_to':obj.release_to,
             'release_lib':obj.release_library,
                     }
                     
        obj_pre_deploy = var_change(str=obj.pre_deploy,**dic_project)
        
        
        
        
        new_file("pre_deploy.sh", obj_pre_deploy)
        new_file("post_deploy.sh", obj.post_deploy)
        new_file("pre_release.sh", obj.pre_release)
        new_file("post_release.sh", obj.post_release)
        create_release_path(hosts=obj.hosts, path=obj_release_dir)
    except:
        exinfo=sys.exc_info()
        logging.error(exinfo)
        ret.append(exinfo)
    
    
    if len(ret) == 0:       
        message = "SUCCESS\nProject:%s\n Env:%s\n配置验证和初始化成功" % (obj_project,obj_env)
        ret.append(message)
  
    return render_to_response("skdeploy/Project_init.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def Project_template(request):
    temp_name = "skdeploy/skdeploy-header.html"    
    tpl_all = Project.objects.filter(template_enable = True)
    
    return render_to_response('skdeploy/Project_template.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def Project_add_from_template(request,ids):
    temp_name = "skdeploy/skdeploy-header.html"
    
    
    if request.method == "POST":
        tpl_Project_form = Project_form(request.POST)
        if tpl_Project_form.is_valid():         
            tpl_Project_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdeploy/Project_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        obj = get_object(Project, id=ids)
        dic_init={
            'desc':obj.desc,
            
            'env':obj.env,
            'group':obj.group,
            'status':obj.status,
            'repo_url':obj.repo_url,
            'repo_mode':obj.repo_mode,
            'repo_type':obj.repo_type,
            'release_user':obj.release_user,
            'release_to':obj.release_to,
            'release_library':obj.release_library,
            'pre_deploy':obj.pre_deploy,
            'post_deploy':obj.post_deploy,
            'pre_release':obj.pre_release,
            'post_release':obj.post_release,
            'post_release_delay':obj.post_release_delay,
            'audit_enable':obj.audit_enable,
            'audit_flow':obj.audit_flow,
            'keep_version_num':obj.keep_version_num,

             }
        print dic_init
        tpl_Project_form = Project_form(initial=dic_init) 
        return render_to_response("skdeploy/Project_add.html", locals(), RequestContext(request))

