#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import AuditFlow,Environment,WorkOrderGroup,WorkOrder,WorkOrderFlow
import os,shutil
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log
from lib.file import new_file

from .forms import WorkOrder_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime

from lib.lib_config import get_config_var
from git import Repo

level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)
git_path = get_dir("git_path")
proj_base_dir = get_dir("pro_path")


@login_required()
@permission_verify()
def WorkOrder_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = WorkOrder.objects.filter(template_enable = False)
    
    return render_to_response('skworkorders/WorkOrder_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrder_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_WorkOrder_form = WorkOrder_form(request.POST)
        if tpl_WorkOrder_form.is_valid():
            
            
          
                
            tpl_WorkOrder_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skworkorders/WorkOrder_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_WorkOrder_form = WorkOrder_form()
        return render_to_response("skworkorders/WorkOrder_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def WorkOrder_del(request):
#    temp_name = "skworkorders/skworkorders-header.html"
    WorkOrder_id = request.GET.get('id', '')
    if WorkOrder_id:
        WorkOrder.objects.filter(id=WorkOrder_id).delete()
    
    if request.method == 'POST':
        WorkOrder_items = request.POST.getlist('x_check', [])
        if WorkOrder_items:
            for n in WorkOrder_items:
                WorkOrder.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')
 #   allworkorder = WorkOrder.objects.all()
    
 #   return render_to_response("skworkorders/WorkOrder.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def WorkOrder_edit(request):
    temp_name = "skworkorders/skworkorders-header.html"
    ids = request.GET.get('id', '')
    obj = get_object(WorkOrder, id=ids)
    
    
    if request.method == 'POST':
        tpl_WorkOrder_form = WorkOrder_form(request.POST, instance=obj)
        if tpl_WorkOrder_form.is_valid():

            obj_env_id=request.POST.get('env') 
            obj_workorder_name = request.POST.get('name')                  
            obj_env_eng=Environment.objects.get(id=obj_env_id)
         
       
            tpl_WorkOrder_form.save()
           
            ret = []
            message = "SUCCESS\n保存成功" 
            ret.append(message)
            tips = u"保存成功！"
            display_control = ""
            return render_to_response("skworkorders/WorkOrder_edit.html", locals(), RequestContext(request))
        else:
            tips = u"保存失败！"
            display_control = ""
            return render_to_response("skworkorders/WorkOrder_edit.html", locals(), RequestContext(request))
    else:
     
        tpl_WorkOrder_form = WorkOrder_form(instance=obj)      
        display_control = "none"
      
        return render_to_response("skworkorders/WorkOrder_edit.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrder_init(request):
    temp_name = "skworkorders/skworkorders-header.html"

    WorkOrder_id = request.GET.get('id')
    obj = get_object(WorkOrder, id=WorkOrder_id)
    obj_env = str(obj.env)
    obj_workorder = obj.name
    obj_type = obj.repo_type
    pre_release_base_path = get_config_var("release_path")
    pre_release_proj_path = pre_release_base_path+obj_env+"/"+obj_workorder+"/"
    
    proj_dir = proj_base_dir+obj_env+"/"+obj_workorder
    ret = []
    if obj.release_library.endswith('/'):
        obj_release_dir = obj.release_library + obj.name
    else:
        obj_release_dir = obj.release_library + "/" + obj.name 
        
    if obj_type == "git":
        repo_path = git_path+obj_env+"/"+obj_workorder

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
        dic_workorder={
             'repo_path':repo_path,
             'pre_release_path':pre_release_proj_path,
             'env':obj_env,
             'workorder':obj_workorder,
             'repo_url':repo_url,
             'release_user':obj.release_user,                
             'release_to':obj.release_to,
             'release_lib':obj.release_library,
                     }
                     
        obj_pre_deploy = var_change(str=obj.pre_deploy,**dic_workorder)
        
        
        
        
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
        message = "SUCCESS\nWorkOrder:%s\n Env:%s\n配置验证和初始化成功" % (obj_workorder,obj_env)
        ret.append(message)
  
    return render_to_response("skworkorders/WorkOrder_init.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def WorkOrder_template(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = WorkOrder.objects.filter(template_enable = True)
    
    return render_to_response('skworkorders/WorkOrder_template.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrder_add_from_template(request,ids):
    temp_name = "skworkorders/skworkorders-header.html"
    
    
    if request.method == "POST":
        tpl_WorkOrder_form = WorkOrder_form(request.POST)
        if tpl_WorkOrder_form.is_valid():         
            tpl_WorkOrder_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skworkorders/WorkOrder_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        obj = get_object(WorkOrder, id=ids)
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
        tpl_WorkOrder_form = WorkOrder_form(initial=dic_init) 
        return render_to_response("skworkorders/WorkOrder_add.html", locals(), RequestContext(request))

