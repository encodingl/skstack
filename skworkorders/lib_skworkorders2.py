#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年7月9日 @author: encodingl
'''
from lib.lib_celery import format_celery_eta_time
from skworkorders.tasks import schedule_task
from skworkorders.models import WorkOrder,WorkOrderFlow,ConfigCenter
from datetime import datetime
from skstack import celery_app
from skaccounts.models import UserInfo
from .lib_skworkorders import custom_task
import json
from skworkorders.lib_skworkorders import format_to_user_vars
import pytz
import logging
# from _mysql import NULL
from lib.com import get_object
from lib.lib_redis import RedisLock
from django.forms.models import model_to_dict


log = logging.getLogger('skworkorders')



    

class WorkOrdkerFlowTask(RedisLock):
    def __init__(self,WorkOrderFlow_id,login_user,request):
        self.obj = WorkOrderFlow.objects.get(id=WorkOrderFlow_id) 
        self.obj2 = WorkOrder.objects.get(id = self.obj.workorder_id)
        
        try:
            self.obj3 = get_object(ConfigCenter, id=self.obj.config_center_id)
            self.config_center_dic = json.dumps(model_to_dict(self.obj3 ))
        except Exception as e:
            self.config_center_dic = None
       
        self.user = login_user
        self.request = request
        self.channel_name = str(self.obj2.name) + "_" + str(self.obj2.env) + "_" + str(self.obj2.id) + "_taskcommit_lock"
      
        RedisLock.__init__(self, self.channel_name)

            
    def celery_task_add(self):
        obj_WorkOrder = WorkOrder.objects.get(id=self.obj.workorder_id)
        taskname_dic = {"main_task":obj_WorkOrder.main_task,"post_task":obj_WorkOrder.post_task}
        taskname_dic = json.dumps(taskname_dic)
        if obj_WorkOrder.var_built_in:
            var_built_in_dic = json.dumps(eval(obj_WorkOrder.var_built_in))
        else:
            var_built_in_dic = {}
            var_built_in_dic = json.dumps(var_built_in_dic)
        user_vars_dic=eval(self.obj.user_vars)
        user_vars_dic = json.dumps(user_vars_dic)
        if self.obj.celery_schedule_time:
            eta_time = format_celery_eta_time(str(self.obj.celery_schedule_time))
        else:
            eta_time = format_celery_eta_time(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        task01 = schedule_task.apply_async((taskname_dic,var_built_in_dic,user_vars_dic,self.config_center_dic), eta=eta_time)

        self.obj.celery_task_id = task01.id
        self.obj.status="CREATED"
        self.obj.save()
        content_str = "添加celery任务成功"
        self.log_celery_id("info", content_str)
        
    def celery_task_revoke(self):
        celery_id = self.obj.celery_task_id
        celery_app.AsyncResult(celery_id).revoke()
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.obj.status="9"
        self.obj.finished_at = time_now
        self.obj.save()
        
    def celery_task_kill(self):
        celery_id = self.obj.celery_task_id
        celery_app.control.revoke(celery_id,terminate=True, signal='SIGKILL')
        
    def celery_task_changeto_manual_task(self):
        
        self.obj.desc = self.obj.desc + "\n" + "原后台任务id:%s 变更为前台手动执行" % self.obj.celery_task_id
        self.obj.save()
        self.celery_task_revoke()
        content_str = "celery task revoked"
        self.log_celery_id("info", content_str)
        msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),content_str),ensure_ascii=False).encode('utf-8')
        self.request.websocket.send(msg)
        

    def permission_submit_pass(self):
         # 判断用户是否有提单权限
        obj_user = UserInfo.objects.get(username=self.user)
        user_group = obj_user.usergroup_set.all()
        user_WorkOrder = WorkOrder.objects.filter(user_dep__in=user_group,status="yes",template_enable = False)
        if self.obj2 in user_WorkOrder:
            return True
        else:
            return False
    def permission_submit_deny(self):
        self.sendmsg("ERROR The Job finished:  failed  \n\r")
        self.log("error", "WARNING The Job finished:  failed")
    
    def task_lock_pass(self):
        if self.obj2.task_lock_enable == False:
            return True
        else:
            if self.is_locked():
                self.sendmsg("ERROR  the system have unfinished task for the sanme project\n\r")
                return False
            else:
                self.lock()  
                return True

        
    def permission_audit_pass(self):
          #判断是否通过审核
        obj_audit_level = self.obj.audit_level
        obj_status = self.obj.status
        if obj_status == "CREATED":
            return True
        else:
            if (obj_audit_level == "1" and obj_status != "1") or (obj_audit_level == "2" and obj_status != "5") or (obj_audit_level == "3" and obj_status != "7") :
                return  False
            else:
                return True
        
    def permission_audit_deny(self):
        content_str = "ERROR You donot have permission\n\r"
        self.sendmsg(content_str)
        self.log("error", content_str)
        
    def sendmsg(self,msg):
        msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),msg),ensure_ascii=False).encode('utf-8')
        self.request.websocket.send(msg) 
           
    def log(self,level,content_str):
        if level == "info":
            log.info("User:%s,Env:%s,WorkOrderName:%s,WorkOrderFlowID:%s,msg:%s" % (self.user,self.obj.env,self.obj2.name,self.obj.id,content_str))
        elif level == "error":
            log.error("User:%s,Env:%s,WorkOrderName:%s,WorkOrderFlowID:%s,msg:%s" % (self.user,self.obj.env,self.obj2.name,self.obj.id,content_str))
        elif level == "warning":
            log.warning("User:%s,Env:%s,WorkOrderName:%s,WorkOrderFlowID:%s,msg:%s" % (self.user,self.obj.env,self.obj2.name,self.obj.id,content_str))
            
    def log_celery_id(self,level,content_str):
        if level == "info":
            log.info("User:%s,Env:%s,WorkOrderName:%s,WorkOrderFlowID:%s,celery_task_id:%s,msg:%s" % \
                     (self.user,self.obj.env,self.obj2.name,self.obj.id,self.obj.celery_task_id,content_str))
        elif level == "error":
            log.error("User:%s,Env:%s,WorkOrderName:%s,WorkOrderFlowID:%s,celery_task_id:%s,msg:%s" % \
                      (self.user,self.obj.env,self.obj2.name,self.obj.id,self.obj.celery_task_id,content_str))
        elif level == "warning":
            log.warning("User:%s,Env:%s,WorkOrderName:%s,WorkOrderFlowID:%s,celery_task_id:%s,msg:%s" % \
                        (self.user,self.obj.env,self.obj2.name,self.obj.id,self.obj.celery_task_id,content_str))
        
       
    def all_task_do(self):
        user_vars_dic = eval(self.obj.user_vars)
        retcode = 0
        if self.obj2.main_task:
            retcode = custom_task(self.obj2, user_vars_dic, self.request,taskname="main_task")
        else:
            content_str = "INFO without main_task to do"
            msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),content_str),ensure_ascii=False).encode('utf-8')
            self.request.websocket.send(msg)
   
        if self.obj2.post_task and retcode==0:
            retcode = custom_task(self.obj2, user_vars_dic, self.request,taskname="post_task")
        else:
            content_str = "INFO without post_task to do"
            msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),content_str),ensure_ascii=False).encode('utf-8')
            self.request.websocket.send(msg)
            
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if retcode == 0:
            self.obj.status="3"
            self.obj.finished_at = obj_finished_at
            self.obj.save()
            content_str = "INFO The Job: finished successful \n\r"
            msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),content_str),ensure_ascii=False).encode('utf-8')
            self.request.websocket.send(msg)
            self.log("info", content_str)
            self.unlock()
            

        else:
            self.obj.status="4"
            self.obj.finished_at = obj_finished_at
            self.obj.save()
            content_str = "ERROR The Job: failed \n\r"
            msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),content_str),ensure_ascii=False).encode('utf-8')
            self.request.websocket.send(msg)
            self.log("error", content_str)
            self.unlock()
            

class PreTask(RedisLock):
    def __init__(self,WorkOrder_id,request,message_dic):
        self.obj = WorkOrder.objects.get(id=WorkOrder_id) 
        self.user = request.user
        self.request = request
        
        self.message_dic_format,self.user_vars_dic = format_to_user_vars(**message_dic)
        self.channel_name = str(self.obj.name) + "_" + str(self.obj.env) + "_" + str(self.obj.id) + "_taskcommit_lock"
        try:
            RedisLock.__init__(self, self.channel_name)
        except Exception as e:
            self.sendmsg("ERROR Failed to connect to redis")

        
        try:
            self.obj3 = get_object(ConfigCenter, id=self.obj.config_center_id)
            self.config_center_dic = json.dumps(model_to_dict(self.obj3 ))
        except Exception as e:
            self.config_center_dic = None
    def sendmsg(self,msg):
        msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),msg),ensure_ascii=False).encode('utf-8')
        self.request.websocket.send(msg)
            
    def log(self,level,content_str):
        if level == "info":
            log.info("User:%s,Env:%s,WorkOrderName:%s,msg:%s" % (self.user,self.obj.env,self.obj.name,content_str))
        elif level == "error":
            log.error("User:%s,Env:%s,WorkOrderName:%s,msg:%s" % (self.user,self.obj.env,self.obj.name,content_str))
        elif level == "warning":
            log.warning("User:%s,Env:%s,WorkOrderName:%s,msg:%s" % (self.user,self.obj.env,self.obj.name,content_str))
    
    def all_task_do(self):
        content_str = "execute starting"
        self.log("info", content_str)
        retcode = 0
        if self.obj.main_task:
            retcode = custom_task(self.obj, self.user_vars_dic, self.request,taskname="main_task")
        else:
            content_str = "INFO main_task: nothing to do \n\r"
            self.log("info", content_str)

        if self.obj.post_task and retcode==0:
            retcode = custom_task(self.obj, self.user_vars_dic, self.request,taskname="post_task")
        else:
            content_str = "INFO post_task: nothing to do \n\r"
            self.log("info", content_str)
            
        obj_finished_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.message_dic_format["finished_at"]=obj_finished_at
    
        if retcode == 0:
            self.message_dic_format["status"] = 3
            self.message_dic_format.pop("celery_schedule_time")
            WorkOrderFlow.objects.create(**self.message_dic_format)
            content_str = "INFO The Job: finished successful \n\r"
            msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),content_str),ensure_ascii=False).encode('utf-8')
            self.request.websocket.send(msg)
            self.log("info", content_str)
            self.unlock()

        else:
            
            self.message_dic_format["status"] = 4
            self.message_dic_format.pop("celery_schedule_time")
            WorkOrderFlow.objects.create(**self.message_dic_format)
            content_str = "ERROR The Job: finished failed \n\r"
            msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),content_str),ensure_ascii=False).encode('utf-8')
            self.request.websocket.send(msg)
            self.log("error", content_str)
            self.unlock()
            
    def celery_task_add(self):
        content_str = "INFO celery tast commit ... \n\r"
        msg = json.dumps("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),content_str),ensure_ascii=False).encode('utf-8')
        self.request.websocket.send(msg)
        time01 = self.message_dic_format["celery_schedule_time"]
        if time01 == "":
            self.sendmsg("warning:请输入计划执行时间   \n\r")
        else:
            time01 = datetime.strptime(time01, "%Y-%m-%d-%H:%M:%S")
            local_tz = pytz.timezone(celery_app.conf['CELERY_TIMEZONE'])
            eta_time = local_tz.localize(datetime.strptime(str(time01).strip(), '%Y-%m-%d %H:%M:%S'))
            taskname_dic = {"main_task":self.obj.main_task,"post_task":self.obj.post_task}
            taskname_dic = json.dumps(taskname_dic)
            if self.obj.var_built_in:
                var_built_in_dic = eval(self.obj.var_built_in) 
            else:
                var_built_in_dic = {}
            var_built_in_dic = json.dumps(var_built_in_dic)
            user_vars_dic = json.dumps(self.user_vars_dic)
            try:
                task01 = schedule_task.apply_async((taskname_dic,var_built_in_dic,user_vars_dic,self.config_center_dic), eta=eta_time)
                self.message_dic_format["celery_task_id"]=task01.id    
                self.message_dic_format["status"] = "CREATED"
                self.message_dic_format["celery_schedule_time"] = time01
                WorkOrderFlow.objects.create(**self.message_dic_format)
                content_str = "INFO The Job Finished:The scheduled task is created successfully \n\r"
                self.sendmsg(content_str)
                self.log("info", content_str)
            except Exception as e:
                self.request.websocket.send("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),e))
                self.log("info", e)
                content_str = "ERROR The Job Failed:the scheduled-task created fialed，for more details，pls see the celery log \n\r"
                self.sendmsg(content_str)
                self.log("info", content_str)
    
    def celery_bgtask_add(self):
        self.sendmsg("INFO celery tast commit ... \n\r")
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      
        eta_time = format_celery_eta_time(str(time_now))
        taskname_dic = {"main_task":self.obj.main_task,"post_task":self.obj.post_task}
        taskname_dic = json.dumps(taskname_dic)
        if self.obj.var_built_in:
            var_built_in_dic = eval(self.obj.var_built_in) 
        else:
            var_built_in_dic = {}
        var_built_in_dic = json.dumps(var_built_in_dic)
        user_vars_dic = json.dumps(self.user_vars_dic)
        try:
            task01 = schedule_task.apply_async((taskname_dic,var_built_in_dic,user_vars_dic,self.config_center_dic), eta=eta_time,serializer='json')
            self.message_dic_format["celery_task_id"]=task01.id    
            self.message_dic_format["status"] = "CREATED"
            self.message_dic_format["celery_schedule_time"] = time_now
            WorkOrderFlow.objects.create(**self.message_dic_format)
            content_str = "INFO The Job Finished:The backgroud-task is created successfully \n\r"
            self.sendmsg(content_str)
            self.log("info", content_str)
        except Exception as e:
            self.request.websocket.send("%s %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),e))
            self.log("info", e)
            content_str = "ERROR The Job Failed:the background-task created faled，for more details，pls see the celery log \n\r"
            self.sendmsg(content_str)
            self.log("info", content_str)
        
            
    def celery_task_create(self):
        time01 = self.message_dic_format["celery_schedule_time"] 
        if time01 == "":
            self.request.websocket.send(json.dumps("warning:请输入计划执行时间",ensure_ascii=False).encode('utf-8'))
        else:
            time01 = datetime.strptime(time01, "%Y-%m-%d-%H:%M:%S")                
            self.message_dic_format["status"] = 0
            self.message_dic_format["celery_schedule_time"] = time01
            WorkOrderFlow.objects.create(**self.message_dic_format)
            content_str = "INFO The Job: submitted successful \n\r"
            self.sendmsg(content_str)
            self.log("info", content_str)
           
            
    def manual_task_add(self):
        self.message_dic_format["status"] = 0
        self.message_dic_format.pop("celery_schedule_time")

        WorkOrderFlow.objects.create(**self.message_dic_format)
        content_str = "INFO The Job: submitted successful \n\r"
        self.sendmsg(content_str)
        self.log("info", content_str)
        
    def task_lock_pass(self):
        if self.obj.task_lock_enable == False:
            self.sendmsg("INFO  the task lock function is not enabled \n\r")
            return True
        else:
          
            if self.is_locked():
                self.sendmsg("ERROR  There are unfinished task for the sanme project\n\r")
                return False
            else:
                self.lock()
                self.sendmsg("INFO  the task-lock is enabled \n\r")
                return True
        
    def permission_submit_pass(self):
        # 判断用户是否有提单权限
        obj_user = UserInfo.objects.get(username=self.user)
        user_group = obj_user.usergroup_set.all()
        user_WorkOrder = WorkOrder.objects.filter(user_dep__in=user_group,status="yes",template_enable = False)
        if self.obj in user_WorkOrder:
            return True
        else:
            return False  
        
    def permission_submit_deny(self):
        self.sendmsg("ERROR The Job finished:  failed  \n\r")
        self.log("error", "WARNING The Job finished:  failed")
    
    def pre_task_success(self):

        if self.obj.pre_task:
            retcode = custom_task(self.obj, self.user_vars_dic, self.request,taskname="pre_task")
        else:
            retcode = 0
            content_str = "INFO pre_task: nothing to do \n\r"
            self.log("info", content_str)
        return True if retcode == 0 else False
#         if retcode == 0:
#             return True
#         else:
#             return False
        
    def pre_task_failed(self):
        content_str = "ERROR The Job finished:  failed  \n\r"
        self.sendmsg(content_str)
        self.log("error", content_str)
       

    
# def celery_schedule_task(WorkOrderFlow_id):
#     obj_WorkOrderFlow = WorkOrderFlow.objects.get(id=WorkOrderFlow_id)
#     obj_WorkOrder = WorkOrder.objects.get(id=obj_WorkOrderFlow.workorder_id)
#     taskname_dic = {"main_task":obj_WorkOrder.main_task,"post_task":obj_WorkOrder.post_task}
#     if obj_WorkOrder.var_built_in:
#         var_built_in_dic = eval(obj_WorkOrder.var_built_in) 
#     else:
#         var_built_in_dic = {}
#     user_vars_dic=eval(obj_WorkOrderFlow.user_vars)
#     format_eta = format_celery_eta_time(str(obj_WorkOrderFlow.celery_schedule_time))
#      
#     task01 = schedule_task.apply_async((taskname_dic,var_built_in_dic,user_vars_dic,self.config_center_dic), eta=format_eta)
#     obj_WorkOrderFlow.celery_task_id = task01.id
#     obj_WorkOrderFlow.status="PENDING"
#     obj_WorkOrderFlow.save()


if __name__ == '__main__':
    eta_time = format_celery_eta_time(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print(eta_time)
    
