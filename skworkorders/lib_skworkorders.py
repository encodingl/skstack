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
from skworkorders.models import VarsGroup,Vars,WorkOrder,WorkOrderFlow
from skworkorders.forms import Vars_Select_form,Custom_form
from lib.lib_format import list_to_formlist
from skcmdb.api import get_object
from subprocess import Popen, PIPE, STDOUT, call
import subprocess
from skaccounts.models import UserInfo,UserGroup,AuditFlow
from datetime import datetime
import commands




level = get_config_var("log_level")
log_path = get_config_var("log_path")
log("setup.log", level, log_path)



def uni_to_str(args):
    obj_uni = args
    obj_list = eval(obj_uni) 
    obj_str=""
    for h in obj_list:
        h=h.strip()
        obj_str=obj_str+h+","
    return obj_str


    
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
        tpl_Custom_form = tpl_Custom_form(initial=content)

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
        obj_value_optional = eval(commands.getoutput(obj.value_script))
        tpl_Custom_form.fields[var_name].widget.choices = list_to_formlist(obj_value_optional) 
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

#该 函数用于将用户选择的变量格式化到一个字典存放到WorkOrderFlow数据库表的user_vars字段中
def format_to_user_vars(**message_dic):
    
    WorkOrder_id = int(message_dic['id'])       
    obj = get_object(WorkOrder, id=WorkOrder_id)
    obj_VarsGroup=VarsGroup.objects.get(name=obj.var_opional)
    user_vars_dic={}

    for obj_var in obj_VarsGroup.vars.all():  
        obj_var_name = str(obj_var.name)
        print message_dic[obj_var_name]
        if message_dic.has_key(obj_var_name):
            
            user_vars_dic[obj_var_name]=message_dic[obj_var_name]
            message_dic.pop(obj_var_name)
    message_dic.pop("csrfmiddlewaretoken")
    message_dic.pop("id")
    print "user_vars:%s" % user_vars_dic
    message_dic["user_vars"]=user_vars_dic
    return message_dic
            
def custom_task(obj_WorkOrder,user_vars_dic,request,taskname):
    obj = obj_WorkOrder
    var_built_in_dic = eval(obj.var_built_in) 
    taskname_dic = {"pre_task":obj.pre_task,"main_task":obj.main_task,"post_task":obj.post_task} 
   
    if taskname_dic[taskname]:
        task = var_change2(taskname_dic[taskname],**user_vars_dic) 
        task = var_change2(task,**var_built_in_dic)
   
        task_list = task.encode("utf-8").split("\r") 
        ret_message="%s:开始执行" % taskname
        request.websocket.send(ret_message)           
        for cmd in task_list:
            pcmd = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            while True: 
                line = pcmd.stdout.readline().strip()  #获取内容
                if line:
                    request.websocket.send(line)
                else:    
                    break
            retcode=pcmd.wait()
            if retcode==0:
                pass
            else:
                ret_message="%s:执行失败" % taskname
                break
        if retcode==0:
            
            ret_message="%s:执行成功" % taskname

        request.websocket.send(ret_message)
    return retcode
         
def permission_submit_pass(user,WorkOrder_id):
    # 判断用户是否有提单权限
    obj_user = UserInfo.objects.get(username=user)
    user_group = obj_user.usergroup_set.all()
    user_WorkOrder = WorkOrder.objects.filter(user_dep__in=user_group,status="yes",template_enable = False)
    obj_WorkOrder = WorkOrder.objects.get(id = WorkOrder_id)
    
    if obj_WorkOrder in user_WorkOrder:
        return True
    else:
        return False
def permission_audit_pass(obj_audit_level,obj_status):
    #判断是否通过审核
    if (obj_audit_level == "1" and obj_status != "1") or (obj_audit_level == "2" and obj_status != "5") or (obj_audit_level == "3" and obj_status != "7") :
        return  False
    else:
        return True
    

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

         
        
        
        
        
        