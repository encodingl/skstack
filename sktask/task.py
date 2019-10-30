#! /usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from .models import project,job,extravars
import os
import re
from skconfig.views import get_dir,get_ansible_config
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from skaccounts.models import RoleJob,UserInfo
import logging
from lib.log import log
from lib.setup import get_playbook, get_roles, get_AnsibleHostsDic,get_IpList,get_hostsFile
from .models import history
from .forms import Project_form
from django.shortcuts import render
from django.template import RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from .models import history
from datetime import datetime
from sktask.models import ONLINE_STATUS


level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)
ansible_dir = get_dir("a_path")






@login_required()
@permission_verify()
def index(request):
    proj_base_dir = get_dir("pro_path")
    inventory = get_ansible_config("inventory")   
    default_check_HostsFile = inventory.split('/')[-1]
    temp_name = "sktask/setup-header.html"
    all_HostsFile = get_hostsFile(ansible_dir)
    all_ansible_hosts_dic,list_key,all_group_key = get_AnsibleHostsDic(inventory)   
    all_ansible_hosts_ip = get_IpList(inventory)
    all_ansible_hosts = all_group_key + all_ansible_hosts_ip   
    all_projects = project.objects.filter(online_status=1)    
    return render(request,'sktask/task.html', locals())

@login_required()
@permission_verify()
def hostfile_change(request):
  
    inventory = request.POST.get('icheck_HostsFile')   
    inventory_abs = ansible_dir+inventory
    all_HostsFile = get_hostsFile(ansible_dir)
    all_ansible_hosts_dic,list_key,all_group_key = get_AnsibleHostsDic(inventory_abs)   
    all_ansible_hosts_ip = get_IpList(inventory_abs)
    icheck_all_ansible_hosts = all_group_key + all_ansible_hosts_ip   
    obj_list = list(icheck_all_ansible_hosts)
    obj_json = json.dumps(obj_list)
    return  HttpResponse(obj_json)
   

@login_required()
@permission_verify()
def job_search(request):
    """
    任务执行模块，先校验所属用户权限，只显示授权的任务
    """
    
    iUser = UserInfo.objects.get(username=request.user)
    if not iUser.is_superuser:
        role_job_permission = RoleJob.objects.get(name=iUser.role_job)
      
        role_job_permission_list = role_job_permission.permission.all()
        matchJob = []
        for j in role_job_permission_list:
            matchJob.append(j)
    
        project_id = request.POST.get('pid')
        obj = job.objects.filter(project=project_id,name__in=matchJob,online_status='1').values('id','name','playbook')
     
    else:
        project_id = request.POST.get('pid')
        obj = job.objects.filter(project=project_id,online_status='1').values('id','name','playbook')
        
   
    obj_list = list(obj)    
    obj_json = json.dumps(obj_list)
    return  HttpResponse(obj_json)

@login_required()
@permission_verify()
def extravars_search(request):
    job_id = request.POST.get('pid')
    obj = extravars.objects.filter(job=job_id,online_status='1').values('id','name','vars')
  
    obj_list = list(obj)
    print(obj_list)

    obj_json = json.dumps(obj_list)

    return  HttpResponse(obj_json)

@login_required()
@permission_verify()
def playbook(request):
    proj_base_dir = get_dir("pro_path")
    
    ret = []
    temp_name = "sktask/setup-header.html"
    h_obj=""
    extra_vars=""
    if request.method == 'POST':
        user=request.user
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
            
        
        if request.POST.get('ansible_hosts'):
            h_obj = request.POST.get('ansible_hosts')
            extra_vars = "hosts=%s" % h_obj
        if request.POST.get('iCheck_extravars'):
            e_obj = request.POST.get('iCheck_extravars')
            extra_vars = extra_vars + " " + e_obj 
            
        if request.POST.get('iCheck_HostsFile'):
            f_obj = request.POST.get('iCheck_HostsFile')   
            print(f_obj)
            f_obj = ansible_dir+f_obj
        
        p_obj = request.POST.get('iCheck_project')
        j_obj = request.POST.get('iCheck_job')
                
        
    playbook_dir = proj_base_dir +  p_obj
    job_obj = playbook_dir +"/"+ j_obj
    if j_obj.endswith('.yml'):
#         cmd = "ansible-playbook"+ " " + "-i" + " " + " " + f_obj + playbook_dir +"/"+ j_obj + " " + "-e '%s'" % extra_vars
        cmd ="ansible-playbook %s -i %s -e '%s'" % (job_obj,f_obj,extra_vars)
     
    elif j_obj.endswith('.ans'):
#         cmd = "bash"+" " + playbook_dir +"/"+ j_obj + " " + h_obj
          hosts_vars = "%s -i %s" % (h_obj,f_obj)
          cmd = "bash %s '%s'" % (job_obj,hosts_vars)
          
    else:
        ret.append("您定义的job任务脚本不符合规范，playbook脚本名称必须以yml结尾，shell封装的ansible命令任务脚本ans结尾")
        
        return render(request, 'sktask/result.html', locals())
        
    

    try:
        time_start= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        
        data = pcmd.communicate()
       
#         ret.append(data)
        ret=data
    
    except:
        exinfo=sys.exc_info()
        logging.error(exinfo)
    retcode=pcmd.poll()
    if retcode==0:
        retcode="success"
    else:
        retcode="failed"
    dic_his={'login_user':user,
             'src_ip':ip,
             'cmd_object':h_obj,
             'cmd':cmd,
             'cmd_result':retcode,
             'cmd_detail':ret[0],                
             'time_task_start':time_start,
#                  'time_task_finished':time_finished,
             'task_name':j_obj}
    history.objects.create(**dic_his)
    return render(request, 'sktask/result.html', locals())
    
@login_required()
@permission_verify()
def playbook_back(request):
    proj_base_dir = get_dir("pro_path")
   
    ret = []
    h_obj=""
    if request.method == 'POST':
        user=request.user
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
#     if request.is_ajax():
        extra_vars=""
        if request.POST.get('ansible_hosts'):
            h_obj = request.POST.get('ansible_hosts')
            extra_vars = "hosts=%s" % h_obj
        if request.POST.get('iCheck_extravars'):
            e_obj = request.POST.get('iCheck_extravars')
          
            extra_vars = extra_vars + " " + e_obj 
            
      
        
        p_obj = request.POST.get('iCheck_project')
        j_obj = request.POST.get('iCheck_job')
        if request.POST.get('iCheck_HostsFile'):
            f_obj = ansible_dir + request.POST.get('iCheck_HostsFile')
                
        
    playbook_dir = proj_base_dir +  p_obj
    job_obj = playbook_dir +"/"+ j_obj
    if j_obj.endswith('.yml'):
#         cmd = "ansible-playbook"+" " + playbook_dir +"/"+ j_obj + " " + "-e '%s'" % extra_vars
        cmd ="ansible-playbook %s -i %s -e '%s'" % (job_obj,f_obj,extra_vars)
    elif j_obj.endswith('.ans'):
#         cmd = "bash"+" " + playbook_dir +"/"+ j_obj + " " + h_obj
        hosts_vars = "%s -i %s" % (h_obj,f_obj)
        cmd = "bash %s '%s'" % (job_obj,hosts_vars)
    else:
        ret.append("您定义的job任务脚本不符合规范，playbook脚本名称必须以yml结尾，shell封装的ansible命令任务脚本ans结尾")
        
        return render(request, 'sktask/result.html', locals())
  
   
    try:
        time_start= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        data = pcmd.communicate()

        ret=data
    
        obj_json = json.dumps(ret)
    except:
        exinfo=sys.exc_info()
        logging.error(exinfo)    
    retcode=pcmd.poll()
    if retcode==0:
        retcode="success"
    else:
        retcode="failed"
    dic_his={'login_user':user,
             'src_ip':ip,
             'cmd_object':h_obj,
             'cmd':cmd,
             'cmd_result':retcode,
             'cmd_detail':ret[0],                
             'time_task_start':time_start,
#                  'time_task_finished':time_finished,
             'task_name':j_obj}
    history.objects.create(**dic_his)

    return  HttpResponse(obj_json)