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
    dic = {}
    pattern = r'^\s*\[.+\]'

    with open(args) as f:
        for line in f:
            temp = line.split()
            if temp:
                m = re.search(pattern,line)

                if (m is not None):
                    g = m.group().strip().strip('[').strip(']')
                    dic[g] = []
                else:
                    try:
                        dic[g].append(line)
                    except:
                        pass
                    
    list_key = []
    dic_list = dic.items()
    list_group_key = dic.keys()
    for key in list_group_key:
        list_key.append(key[0])
    list_key_set=list(set(list_key))
    list_key_set.sort()
    list_group_key.sort()

    return dic_list,list_key_set,list_group_key




def get_IpList(args):

    list_ip=[]
    ip_pattern=r'([0-9]{1,3}\.){3}[0-9]{1,3}'
    
 
    

    f=open(args)

    for line in f:
        m=re.search(ip_pattern,line)
        if(m is not None):
            ip=m.group()
            list_ip.append(ip)
            
            
    f.close()
  
    return list_ip
        
if __name__ == "__main__":
    dic_list,list_key_set,list_group_key=get_AnsibleHostsDic('/etc/ansible/hosts-prd')
    list_ip=get_IpList('/etc/ansible/hosts-prd')
  
    print  dic["yycs"]
   
    
    