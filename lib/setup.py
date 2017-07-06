#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from __builtin__ import list


def get_roles(args):
    dir_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isfile(args+d):
            pass
        else:
            dir_list.append(d)
    return dir_list


def get_playbook(args):
    files_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isdir(args+d):
            pass
        elif d.endswith(".retry"):
            os.remove(args+d)
        else:
            files_list.append(d)
    return files_list


def get_scripts(args):
    files_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isdir(args+d):
            pass
        else:
            files_list.append(d)
    return files_list

def get_hostsFile(args):
    files_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if os.path.isdir(args+d):
            pass
        elif "hosts" in d:
            files_list.append(d)
    return files_list

def get_AnsibleHostsDic(args):
    dic={}
    list_key=[]
    list_group_key=[]
    pattern=r'^\s*\[.+\]'
    
 
    

    f=open(args)

    for line in f:
        m=re.search(pattern,line)
        if(m is not None):
            g=m.group().strip().strip('[').strip(']')
            
            
            p=r'\s*\[%s\](.*?)\n\s*\[.*\]' % g
            
            f1=open(args)
            fstr=f1.read()
            
            h=re.findall(p,fstr,re.S)
           
            f1.close()
            if  h:
                h=h[0].split('\n')
                for i in h:
                    if i=='':
                        h.remove(i)
    #             print "%s:%s" % (g,h)
                dic[g] = h

            
            
            
    f.close()
    
    dic_list = sorted(dic.items(), key=lambda d:d[0])
#     print dic_list
    for key in dic_list:
        list_key.append(key[0][0])
        list_group_key.append(key[0])
    list_key_set=list(set(list_key))
    list_key_set.sort()
    list_group_key.sort()    
    return dic_list,list_key_set,list_group_key
  
        
if __name__ == "__main__":
    get_AnsibleHostsDic('/etc/ansible/hosts-prd')
    a=get_hostsFile("/etc/ansible")
    print a
   
    
    