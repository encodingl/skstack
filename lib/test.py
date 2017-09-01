#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE, STDOUT, call
import re


if __name__ == "__main__":
    cmd = "ansible yunwei61 -m script -a '/opt/scripts/linkread.py'"
    pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)    
   
    retcode_message=pcmd.communicate()
    r1 = retcode_message[0]
    print r1
    a = r1.split(" => ")[1]
    print a
    true = "true"
    dic = eval(a)
    b = dic["stdout_lines"][0]
    print b
#     print r1
#     pattern=r'\s*\{(.*?)\n\s*\}'
#     a = re.findall(pattern, r1,re.S)
#     print a.group()
        

