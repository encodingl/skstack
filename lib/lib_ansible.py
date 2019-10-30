#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017-09-13 17:46:59;  @author: LZ
'''


import configparser
import os
import re
from lib.com import  configfile


def get_AnsibleHostsList(hostsfile,group):
    dic = {}
    pattern = r'^\s*\[.+\]'
    with open(hostsfile) as f:
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
    
    list_tumple_hosts = []
    for h in dic[group]:
        t1=(h,h)
        list_tumple_hosts.append(t1)
    if list_tumple_hosts is None:
        list_tumple_hosts = [('1','ansible hosts没有找到主机'),]
    return list_tumple_hosts

def get_ansible_config_var(args):
    config = configparser.RawConfigParser()
#     dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(configfile, 'r') as cfgfile:
        config.readfp(cfgfile)
        a_path = config.get('config', 'ansible_path')
        
        

    with open(a_path+'/ansible.cfg', 'r') as f:
        config.readfp(f)
        obj_var = config.get('defaults', args)
    return obj_var

   


if __name__ == "__main__":
    yycs_list = get_AnsibleHostsList('/etc/ansible/hosts-prd', "yycs")
    print(get_ansible_config_var("inventory"))
  
    