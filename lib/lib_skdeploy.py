#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lib.lib_config import get_config_var
from lib.log import log
import logging
from subprocess import Popen, PIPE, STDOUT, call
import sys

import os
from lib.lib_config import get_config_var



level = get_config_var("log_level")
log_path = get_config_var("log_path")
log("setup.log", level, log_path)





def adv_task_step(hosts,env,project,task_file):
    proj_base_dir = get_config_var("pro_path")
    task_file_abs = proj_base_dir+env+"/"+project+"/"+task_file
    
    if hosts == "localhost":
        
        cmd = "bash" + " " + task_file_abs
     
        
    else:
#         dest_file_abs="/tmp/%s/%s/%s" % (env,project,task_file)
#         cmd_copy = "ansible %s -m copy -a 'src=%s dest=%s'" %  (hosts,task_file_abs, dest_file_abs)
#         
#         pcmd_copy = Popen(cmd_copy, stdout=PIPE, stderr=PIPE, shell=True)
#         retcode=pcmd_copy.wait()
#         retcode_message=pcmd_copy.communicate()
#         print "1:%s" % retcode_message
#         if retcode==0:         
        cmd = "ansible %s -m script -a %s" % (hosts,task_file_abs)    
    try:        
        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)    
        retcode=pcmd.wait()  
        retcode_message=pcmd.communicate()
        print retcode_message
    
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
    release_palybook=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/scripts/skdeploy/release_project.yml"
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

def change_link(hosts,release_dir,release_to):
    change_link_palybook=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/scripts/skdeploy/change_link.yml"
    cmd= "ansible-playbook  %s -e 'h=%s release_dir=%s release_to=%s'" %  (change_link_palybook,hosts, release_dir,release_to)
    
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
    
if __name__ == "__main__":
    
   
    
    result_pre_deploy = adv_task_step(hosts="localhost", env="prod", project="yyappgw", task_file="post_deploy.sh") 
    print result_pre_deploy
    print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/script/skdeploy/release_project.yml"

         
        
        
        
        
        