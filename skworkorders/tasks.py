#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年7月2日 @author: encodingl
'''

# Create your tasks here

from celery import shared_task
from skworkorders.lib_skworkorders import var_change2
import subprocess
import json
import logging
from lib.lib_fabric import ssh_cmd_back
log = logging.getLogger('skworkorders')


@shared_task
def add(x, y):
    return x + y


@shared_task
def schedule_task(taskname_dic,var_built_in_dic,user_vars_dic,cc_dic):
    retcode = 0
    msg_result_dic={}
    taskname_dic = json.loads(taskname_dic)
    var_built_in_dic = json.loads(var_built_in_dic)
    user_vars_dic = json.loads(user_vars_dic)
    if cc_dic is None:
        pass
    else:
        cc_dic = json.loads(cc_dic)
    
    for taskname,taskvalue in list(taskname_dic.items()):
        if taskvalue:
            task = var_change2(taskvalue,**user_vars_dic) 
            task = var_change2(task,**var_built_in_dic)
            task_list = task.encode("utf-8").split("\r") 
            ret_message="%s:开始执行" % taskname
            log.info(ret_message)   
            if cc_dic is None:    
                for cmd in task_list:
                    try:
                        log.info("cmd_start:%s"  % cmd )
                        pcmd = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
                        retcode=pcmd.wait()  
                        retcode_message=pcmd.communicate()
                        msg_result_dic[taskname]=retcode_message
                    except Exception as msg:
                        log.error("cmd_result:%s" % msg)
                        raise RuntimeError(str(retcode_message).decode("string_escape"))
            else:
                
                for cmd in task_list:
                
                    try:
                        log.info("ssh_cmd_start:%s config_center_ip:%s"  % (cmd,cc_dic["ip"]))
                        retcode_message,retcode = ssh_cmd_back(cc_dic["ip"],cc_dic["port"],cc_dic["username"],cc_dic["password"],cmd,cc_dic["rsa_key"])
                        msg_result_dic[taskname]=retcode_message
                    except Exception as msg:
                        log.error("ssh_cmd_result2:%s" % msg)
                    
            if retcode==0:
                ret_message="%s:执行成功" % taskname
                log.info(ret_message)
            else:
                ret_message="%s:执行失败" % taskname
#     msg_result_dic = json.dumps(msg_result_dic,ensure_ascii=False).encode('utf-8')
#     print "jsonstrL:%s" % msg_result_dic
    print("msg_result_dic:%s" % msg_result_dic)
    return msg_result_dic
        