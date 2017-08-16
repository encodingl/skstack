#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lib.lib_config import get_config_var
from lib.log import log
import logging
from subprocess import Popen, PIPE, STDOUT, call
import sys




level = get_config_var("log_level")
log_path = get_config_var("log_path")
log("setup.log", level, log_path)



def adv_task_step(hosts,env,project,task_file):
    proj_base_dir = get_config_var("pro_path")
    task_file_abs = proj_base_dir+env+"/"+project+"/"+task_file
    
    if hosts == "localhost":
        
        cmd = "bash" + " " + task_file_abs
        
    else:
        dest_file_abs="/tmp/%s/%s/%s" % (env,project,task_file)
        cmd_copy = "ansible %s -m copy -a 'src=%s dest=%s'" %  (hosts,task_file_abs, dest_file_abs)
        
        pcmd_copy = Popen(cmd_copy, stdout=PIPE, stderr=PIPE, shell=True)
        retcode=pcmd_copy.poll()
        if retcode==0:
            pass
        else:
            ret_message="failed"
            return ret_message
        
        
        cmd = "ansible %s -m script -a '%s'" % (hosts,dest_file_abs)
        
    try:        
        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)      
 

     
    except:
        exinfo=sys.exc_info()
        logging.error(exinfo)
    retcode=pcmd.poll()
    if retcode==0:
        ret_message="success"
    else:
        ret_message="failed"
    return ret_message
if __name__ == "__main__":
    adv_task_step(hosts="yyappgw",env="prod",project="yyappgw",task_file="post_deploy.sh")
    print "haha"
        
        
        
        
        
        