#! /usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse
from .models import AuditFlow,Environment,WorkOrder,WorkOrderFlow
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from .forms import WorkOrderCommit_form,WorkOrderCommit_help_form
from django.shortcuts import render
from django.template import RequestContext
from skcmdb.api import get_object

from datetime import datetime
import json
from skaccounts.models import UserInfo
from django import forms
#from dwebsocket.decorators import accept_websocket
from skworkorders.lib_skworkorders import get_VarsGroup_form,format_to_user_vars,custom_task,permission_submit_pass
from skworkorders.lib_skworkorders2 import PreTask
from lib.lib_json import my_obj_pairs_hook
from datetime import datetime,timedelta
import pytz
from skworkorders import tasks
from skstack.celery import app as celery_app
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer,JsonWebsocketConsumer
import json
import logging
from _ast import Await
log = logging.getLogger('skworkorders')


from channels.generic.websocket import AsyncWebsocketConsumer
from skworkorders.test_websocket import TestWebSend




class pretask(AsyncWebsocketConsumer):
 
    async def connect(self):
        self.group_name = "group_test_01"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        p1 = TestWebSend(self.group_name,"call out")
        p1.sendmsg()
#         print(text_data)
#         message = json.loads(text_data)
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'show_in_windows',
#                 'message': message
#             }
#         )
    async def show_in_windows(self,event):
#         print(event)
        print("7")
        message = event["message"]
        print(message)
        await self.send(text_data=json.dumps({
            "message":message}))
    async def disconnect(self, close_code):
        pass
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)
#         print("disconnected")
#         message = json.loads(text_data)
#         print(self.channel_name)
#         pt01 = TestWebSend(message,self.channel_name)
#         
#         pt01.sendmsg()
#                
        
#         self.send("The task has been submitted, please wait patiently·······")
#         message_dic = json.loads(message,object_pairs_hook=my_obj_pairs_hook)
#         
#         WorkOrder_id = int(message_dic['id'])
#         pt01 = PreTask(WorkOrder_id,request,message_dic)
#         if pt01.permission_submit_pass():
#             if pt01.pre_task_success():
#                 if pt01.obj.audit_enable == True:
#                     if pt01.obj.schedule_enable == True: 
#                         pt01.celery_task_create()
#                     else:
#                         pt01.manual_task_add()
#                 else:
#                     if  pt01.obj.schedule_enable == True:
#                         pt01.celery_task_add()
#                     elif pt01.obj.back_exe_enable == True:
#                         if "back_exe_enable" in pt01.message_dic_format:
#                             pt01.celery_bgtask_add()
#                         else:
#                             pt01.all_task_do()
#                              
#                     else:
#                         pt01.all_task_do()
#         
#             else:
#                 pt01.pre_task_failed()
#         else:
#             pt01.permission_submit_deny()
        
        await self.send("2")
        
    async def disconnect(self,close_code):
        pass
#    

# def pretask(request):
#     temp_name = "skworkorders/skworkorders-header.html" 
#     if not request.is_websocket():#判断是不是websocket连接
#         try:#如果是普通的http方法
#             message = request.GET['message']
#             return HttpResponse(message)
#         except:
#             return render(request,'skworkorders/websocket.html', locals())
#     else:
#         for message in request.websocket:    
#             request.websocket.send("The task has been submitted, please wait patiently·······")
#             message_dic = json.loads(message,object_pairs_hook=my_obj_pairs_hook)
# 
#             WorkOrder_id = int(message_dic['id'])
#             pt01 = PreTask(WorkOrder_id,request,message_dic)
#             if pt01.permission_submit_pass():
#                 if pt01.pre_task_success():
#                     if pt01.obj.audit_enable == True:
#                         if pt01.obj.schedule_enable == True: 
#                             pt01.celery_task_create()
#                         else:
#                             pt01.manual_task_add()
#                     else:
#                         if  pt01.obj.schedule_enable == True:
#                             pt01.celery_task_add()
#                         elif pt01.obj.back_exe_enable == True:
#                             if "back_exe_enable" in pt01.message_dic_format:
#                                 pt01.celery_bgtask_add()
#                             else:
#                                 pt01.all_task_do()
#                                 
#                         else:
#                             pt01.all_task_do()
# 
#                 else:
#                     pt01.pre_task_failed()
#             else:
#                 pt01.permission_submit_deny()