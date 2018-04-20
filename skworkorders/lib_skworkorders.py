#! /usr/bin/env python
# -*- coding: utf-8 -*-
import django
django.setup()


from lib.lib_config import get_config_var
from lib.log import log
import logging
from subprocess import Popen, PIPE, STDOUT, call
import sys
from django import forms
import os
from lib.lib_config import get_config_var
from skworkorders.VarsGroup import VarsGroup_add
from skworkorders.models import VarsGroup,Vars
from skworkorders.forms import Vars_Select_form,Custom_form
from lib.lib_format import list_to_formlist




level = get_config_var("log_level")
log_path = get_config_var("log_path")
log("setup.log", level, log_path)

def adv_task_step(hosts,env,project,task_file,forks=30):
    proj_base_dir = get_config_var("pro_path")
    task_file_abs = proj_base_dir+env+"/"+project+"/"+task_file
    
    if hosts == "localhost":
        
        cmd = "bash" + " " + task_file_abs
     
        
    else:

        cmd = "ansible %s -f %s -m script -a %s" % (hosts,forks,task_file_abs)  
        
    try:        
        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)    
        retcode=pcmd.wait()  
        retcode_message=pcmd.communicate()
        
    
    except:
        exinfo=sys.exc_info()
        logging.error(exinfo)
    
    
    if retcode==0:
        ret_message="success"
    else:
        ret_message="failed"
    return ret_message
#         else:
#             ret_message="failed"
#             return ret_message
        
        
    


def release_project(project,env,hosts,release_dir,release_to):
    release_path = get_config_var("release_path")
    project_dir = release_path+env+"/"+project+"/"
    release_palybook=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/scripts/skworkorders/release_project.yml"
    cmd= "ansible-playbook  %s -e 'h=%s project_dir=%s release_dir=%s'" %  (release_palybook,hosts,project_dir, release_dir)
    
    try:        
        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)    
        retcode=pcmd.wait()  
        ret_message = pcmd.communicate()
        
        if retcode != 0:    
            logging.error(ret_message)
        else:
            logging.info(ret_message)
 

     
    except:
        exinfo=sys.exc_info()
        logging.error(exinfo)
    
    
    if retcode==0:
        ret_message="success"
    else:
        ret_message="failed"
    return ret_message

def uni_to_str(args):
    obj_uni = args
    obj_list = eval(obj_uni) 
    obj_str=""
    for h in obj_list:
        h=h.strip()
        obj_str=obj_str+h+","
    return obj_str

def create_release_path(hosts,path):
    
    cmd= "ansible  %s -m shell -a 'mkdir -p %s'" %  (hosts,path)
    
    try:        
        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)    
        retcode=pcmd.wait()  
        ret_message = pcmd.communicate()
        
        if retcode != 0:    
            logging.error(ret_message)
        else:
            logging.info(ret_message)
 
    except:
        exinfo=sys.exc_info()
        logging.error(exinfo)
    
    if retcode==0:
        ret_message="success"
    else:
        ret_message="failed"
    return ret_message

def var_change(str,**pDic):
    str=str.replace("{repo_path}",pDic["repo_path"])
    str=str.replace("{pre_release_path}",pDic["pre_release_path"])
    str=str.replace("{release_to}",pDic["release_to"])
    str=str.replace("{release_lib}",pDic["release_lib"])
    str=str.replace("{project}",pDic["project"])
    str=str.replace("{env}",pDic["env"])
    str=str.replace("{repo_url}",pDic["repo_url"])
    str=str.replace("{release_user}",pDic["release_user"])
    return str
    
def get_Vars_form(obj_var):
    obj=obj_var
#判断表单格式生成合适表单    
    var_name = obj.name
    content = {}
    new_fields = {
            var_name: forms.ChoiceField(label=u'变量名', error_messages={'required': u'不能为空'},widget=forms.Select(attrs={'class': 'form-control'}))
            }
    if obj.value_form_type == "Select":
        tpl_Custom_form = type('tpl_Custom_form', (Custom_form,),  new_fields)
        tpl_Custom_form = tpl_Custom_form(content)

    elif obj.value_form_type == "SelectMultiple":
        pass
    elif obj.value_form_type == "TextInput":
        pass
    elif obj.value_form_type == "Textarea":
        pass
    else:
        pass
  
#判断变量来源获取变量内容    
    if obj.value_method == "admin_def":
        obj_value_optional = eval(obj.value_optional)       
        tpl_Custom_form.fields[var_name].widget.choices = list_to_formlist(obj_value_optional)       
    elif obj.value_method == "script":
        pass
    elif obj.value_method == "manual":
        pass
    tpl_Custom_form.fields[var_name].label = obj.label_name   
    return tpl_Custom_form
    
def get_VarsGroup_form(args):  
  
    obj_VarsGroup=VarsGroup.objects.get(name=args)

    tpl_custom_form = []
   
    for obj_var in obj_VarsGroup.vars.all():
        obj_var_form = get_Vars_form(obj_var)
     
        tpl_custom_form.append(obj_var_form)
        
    return tpl_custom_form  
#     for form in tpl_custom_form:
#         print form
        
     

def var_change2(arg,**kwargs):
    for key,value in kwargs.items():       
        key = "{%s}" % key
        value = str(value)
        arg=arg.replace(key,value)
    return arg


if __name__ == "__main__":
    d = {"a":"avalue","b":"bvalue","c":1}
    s = "{a} whata {b} fk {c}"
    print var_change2(s,**d)
#      get_VarsGroup_form("vg1_stg")
#     cmd1 = "ansible gtest -m shell -a 'du -sh /focus'"
#     cmd2 = "du -sh /focus"
#     cmd3 = "ansible localhost -m shell -a 'du -sh /focus'"
#     list_cmd = [cmd1,cmd2,cmd3]
#     for cmd1 in list_cmd:
#         pcmd1 = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)    
#         retcode1=pcmd1.wait()  
#         retcode_message1=pcmd1.communicate()
#         print retcode1
#         print retcode_message1
#         print retcode_message1[0]
#         print retcode_message1[1]
#        
     
    
   
    
#     result_pre_deploy = adv_task_step(hosts="localhost", env="prod", project="yyappgw", task_file="post_deploy.sh") 
#     print result_pre_deploy
#     print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/script/skworkorders/release_project.yml"

         
        
        
        
        
        