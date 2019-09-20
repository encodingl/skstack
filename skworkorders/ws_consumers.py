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
from channels.generic.websocket import WebsocketConsumer
import json
import logging
log = logging.getLogger('skworkorders')



class pretask(WebsocketConsumer):
   
    def connect(self):
        self.accept()
        
    def disconnect(self, close_code):
        pass    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = 'channels test:' + text_data_json['ws return']
        self.send(text_data=json.dumps({
            'message': message
        }))
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
