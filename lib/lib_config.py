#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import re
from lib.com import  configfile

def get_redis_config():
    config = ConfigParser.RawConfigParser()
#     dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(configfile, 'r') as cfgfile:
        config.readfp(cfgfile)
        host = config.get('redis', 'host')     
        port = config.get('redis', 'port')
        db = config.get('redis', 'db')
        password = config.get('redis', 'password')
        
    if not host:
        host="127.0.0.1"
    if not port:
        port="6379"
    if not db:
        db="0"
    return host,port,db,password

def get_config_var(args):
    config = ConfigParser.RawConfigParser()
#     dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(configfile, 'r') as cfgfile:
        config.readfp(cfgfile)
        a_path = config.get('config', 'ansible_path')
        pro_path = config.get('config', 'project_base_path')
        git_path = config.get('config', 'git_base_path')
        release_path = config.get('config', 'release_base_path')
        token = config.get('token', 'token')
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')

    if args == "a_path":
        return a_path
    if args == "pro_path":
        return pro_path
    if args == "token":
        return token
    if args == "log_path":
        return log_path
    if args == "log_level":
        return log_level
    if args == "git_path":
        return git_path
    if args == "release_path":
        return release_path

def get_AnsibleHostsDic_only(args):
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
    

    return dic
if __name__ == "__main__":
    x = get_redis_config()
    print x