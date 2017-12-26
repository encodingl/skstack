#! /usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT, call
import os

def new_file(file_name,file_content):
    with open(file_name,"a+") as f:
        f.write(file_content)
        
        
def get_ex_link(hosts,dir):
    script_link_read = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/scripts/skdeploy/linkread.py"
    cmd = "ansible %s -m script -a '%s -r %s'" % (hosts,script_link_read,dir)
    pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)     
    retcode_message=pcmd.communicate()
    r1 = retcode_message[0]
    print r1
    r2 = r1.split(" => ")[1]
    print r2
    true = "true"
    dic = eval(r2)
    ex_link = dic["stdout_lines"][0]
    
    return ex_link

if __name__ == "__main__":
    print get_ex_link(hosts="yyappgw", dir="/opt/soft/tomcat/yyappgw/webapps/ROOT")