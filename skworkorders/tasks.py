#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年7月2日 @author: skipper
'''

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from skworkorders.lib_skworkorders import var_change2
import subprocess
import json
import logging
log = logging.getLogger('skworkorders')


@shared_task
def add(x, y):
    return x + y


@shared_task
def schedule_task(taskname_dic,var_built_in_dic,user_vars_dic):
    retcode = 0
    msg_result_dic={}
    taskname_dic = json.loads(taskname_dic)
    var_built_in_dic = json.loads(var_built_in_dic)
    user_vars_dic = json.loads(user_vars_dic)
    for taskname,taskvalue in taskname_dic.items():
        if taskvalue:
            task = var_change2(taskvalue,**user_vars_dic) 
            task = var_change2(task,**var_built_in_dic)
            task_list = task.encode("utf-8").split("\r") 
            ret_message="%s:开始执行" % taskname
            log.info(ret_message)      
            for cmd in task_list:
                try:
                    log.info("cmd_start:%s"  % cmd )
                    pcmd = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
                    retcode=pcmd.wait()  
                    retcode_message=pcmd.communicate()
                    msg_result_dic[taskname]=retcode_message
                except Exception, msg:
                    log.error("cmd_result:%s" % msg)
                    raise RuntimeError(str(retcode_message).decode("string_escape"))
            if retcode==0:
                ret_message="%s:执行成功" % taskname
                log.info(ret_message)
            else:
                ret_message="%s:执行失败" % taskname
#     msg_result_dic = json.dumps(msg_result_dic,ensure_ascii=False)
#     print "jsonstrL:%s" % msg_result_dic
    return msg_result_dic
        