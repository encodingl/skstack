#! /usr/bin/env python
# -*- coding: utf-8 -*-
import django
# from _mysql import NULL
django.setup()

from django import forms
import traceback

from skworkorders.models import VarsGroup,WorkOrder,ConfigCenter
from skworkorders.forms import Custom_form
from skcmdb.api import get_object
from lib.lib_format import list_to_formlist
from lib.lib_paramiko import ssh_cmd
from subprocess import Popen, PIPE, STDOUT
from skaccounts.models import UserInfo

import subprocess
import json
from datetime import datetime
import logging
log = logging.getLogger('skworkorders')



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

    if obj.value_form_type == "Select":
        new_fields = {
            var_name: forms.ChoiceField(label='变量名', error_messages={'required': '不能为空'},widget=forms.Select(attrs={'class': 'form-control'}))
            }
           
    elif obj.value_form_type == "RadioSelect":
        new_fields = {
            var_name: forms.ChoiceField(label='变量名', error_messages={'required': '不能为空'},widget=forms.RadioSelect(attrs={'class': 'list-group'}))
            }       

    elif obj.value_form_type == "SelectMultiple":
        new_fields = {
            var_name: forms.MultipleChoiceField(label='变量名',error_messages={'required': '不能为空'},widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
            }
        
    elif obj.value_form_type == "CheckboxSelectMultiple":
        new_fields = {
            var_name: forms.MultipleChoiceField(label='变量名',error_messages={'required': '不能为空'},widget=forms.CheckboxSelectMultiple(attrs={'class': 'list-group'}))
            }
        
    elif obj.value_form_type == "TextInput":
        new_fields = {
            var_name: forms.CharField(label='变量名', error_messages={'required': '不能为空'},widget=forms.TextInput(attrs={'class': 'form-control'}))
            }
    elif obj.value_form_type == "Textarea":
        new_fields = {
            var_name: forms.CharField(label='变量名', error_messages={'required': '不能为空'},widget=forms.Textarea(attrs={'class': 'form-control'}))
            }
    else:
        pass
    
    tpl_Custom_form = type('tpl_Custom_form', (Custom_form,),  new_fields)
    tpl_Custom_form = tpl_Custom_form(initial=content)
     
#判断变量来源获取变量内容    
    
    if obj.value_method == "admin_def":
        obj_value_optional = eval(obj.value_optional)       
        tpl_Custom_form.fields[var_name].widget.choices = list_to_formlist(obj_value_optional)       
    elif obj.value_method == "script":
        l1 = subprocess.getoutput(obj.value_script)
        obj_value_optional = eval(l1)
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
#     for form in tpl_custom_form:
#         print(form)    
    return tpl_custom_form  
    
        
def dynamic_column_data(queryset_Environment,WorkOrderFlow,date_range):
    tpl_dic_obj={}
    tpl_dic_column={}
    for e in queryset_Environment:
        obj = WorkOrderFlow.objects.filter(env=e.name_english,created_at__range=date_range,celery_task_id__isnull=True).values("id","title","user_vars","workorder_group","user_commit","finished_at","status")
        tpl_list_obj = []
        tpl_list_columns = []
    
        for x in obj:
    
            show_dic = {}
            for k,v in x.items():
                
                if k == "user_vars":
                    v = json.loads(v)
                    for k2,v2 in v.items():
                      
                        show_dic[k2] = v2
                else:
                    show_dic[k] = v
            tpl_list_obj.append(show_dic)
        try:
            for x2 in tpl_list_obj[0].keys():
                
                tpl_list_columns.append(x2)
        
        except IndexError:
            pass    
        tpl_dic_obj[e.name_english]=tpl_list_obj
        tpl_dic_column[e.name_english]=tpl_list_columns
    return tpl_dic_column,tpl_dic_obj
    

def var_change2(arg,**kwargs):
    for key,value in list(kwargs.items()):       
        key = "{%s}" % key
        value = str(value)
        arg=arg.replace(key,value)
    return arg

#该 函数用于将用户选择的变量格式化到一个字典存放到WorkOrderFlow数据库表的user_vars字段中
def format_to_user_vars(**message_dic):    
    WorkOrder_id = int(message_dic['id'])       
    obj = get_object(WorkOrder, id=WorkOrder_id)
    if obj.var_opional_switch == True and obj.var_opional is not None:
        user_vars_dic={}
        obj_VarsGroup=VarsGroup.objects.get(name=obj.var_opional)
        for obj_var in obj_VarsGroup.vars.all():  
            obj_var_name = str(obj_var.name)
            if obj_var_name in message_dic:
                
                user_vars_dic[obj_var_name]=message_dic[obj_var_name]
                message_dic.pop(obj_var_name)
    else: 
        user_vars_dic={}

    
    message_dic.pop("csrfmiddlewaretoken")
    message_dic.pop("id")
    message_dic["user_vars"] = str(json.dumps(user_vars_dic))
    if "back_exe_enable" in message_dic:
        if message_dic["back_exe_enable"] == "on":
            message_dic["back_exe_enable"] = 1
        if message_dic["back_exe_enable"] == "False":
            message_dic["back_exe_enable"] = 0  
    if message_dic["auto_exe_enable"] == "on":
        message_dic["auto_exe_enable"] = 1
    if message_dic["auto_exe_enable"] == "False":
        message_dic["auto_exe_enable"] = 0
    return message_dic,user_vars_dic
            
def custom_task(obj_WorkOrder,user_vars_dic,request,taskname):
    obj = obj_WorkOrder 
    obj2 = get_object(ConfigCenter, id=obj.config_center_id)
    taskname_dic = {"pre_task":obj.pre_task,"main_task":obj.main_task,"post_task":obj.post_task} 
    if taskname_dic[taskname]:       
        task = var_change2(taskname_dic[taskname],**user_vars_dic) 
        if obj.var_built_in:
            var_built_in_dic = eval(obj.var_built_in) 
            task = var_change2(task,**var_built_in_dic)
        task_list = task.split("\r") 
        print(task_list)
        ret_message="INFO %s:start \n\r" % taskname
        log.info(ret_message)
        

        if obj.config_center in [None]:
            for cmd in task_list:
                print(cmd)
                try:
                    log.info("cmd_start:%s"  % cmd )
                    pcmd = Popen(cmd,stdout=PIPE,stderr=STDOUT,shell=True)
                    while True:
                        for line in iter(pcmd.stdout.readline,b''):
                            line = str(line, encoding='utf-8').replace('\n', "\n\r");
                            request.websocket.send(json.dumps(line,ensure_ascii=False).encode('utf-8'))
                        if pcmd.poll() is not None:
                            break  
                except Exception as msg:
                    log.error("cmd_result:%s" % msg)
                    msg = "ERROR %s \n\r" % msg
                    msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),msg),ensure_ascii=False).encode('utf-8')
                    request.websocket.send(msg)
                    return 1

                retcode=pcmd.wait()
               
                if retcode==0:
                    ret_message="INFO %s: succesfull \n\r" % taskname
                    
                else:
                    ret_message="ERROR %s: failed \n\r" % taskname
                    
                    log.error(ret_message)
                    break
        else:
            for cmd in task_list:
                
                try:
                    log.info("ssh_cmd_start:%s config_center_ip:%s"  % (cmd,obj2.ip))
                    retcode = ssh_cmd(obj2.ip,obj2.port,obj2.username,obj2.password,cmd,obj2.rsa_key,request)
                except Exception as msg:
                    log.error("ssh_cmd_result:%s" % msg)
                    retcode = 1111
                if retcode == 0:          
                    ret_message="INFO %s:successful \n\r" % taskname
                    log.info(ret_message)
                else:
                    ret_message="ERROR %s: faild \n\r" % taskname
        
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
    pass


         
        
        
        
        
        