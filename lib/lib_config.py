#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os


def get_redis_config():
    config = ConfigParser.RawConfigParser()
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(dirs+'/skipper.conf', 'r') as cfgfile:
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
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(dirs+'/skipper.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        a_path = config.get('config', 'ansible_path')
        pro_path = config.get('config', 'project_base_path')
        git_path = config.get('config', 'git_base_path')
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

if __name__ == "__main__":
    x = get_redis_config()
    print x