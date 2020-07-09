#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect
from django.template import RequestContext
import configparser
import os
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.contrib.auth import get_user_model
import logging
from lib.log import dic
from lib.com import config, configfile


@login_required()
@permission_verify()
def index(request):
    temp_name = "skconfig/config-header.html"
    display_control = "none"
    all_level = dic
    cfg = config()

    if request.method == 'POST':
        # path
        a_path = request.POST.get('ansible_path')
        pro_path = request.POST.get('project_base_path')
        git_path = request.POST.get('project_base_path')
        engine = request.POST.get('engine')
        host = request.POST.get('host')
        port = request.POST.get('port')
        user = request.POST.get('user')
        password = request.POST.get('password')
        database = request.POST.get('database')
        # cmdb_api_token
        token = request.POST.get('token')
        # log
        log_path = request.POST.get('log_path')
        log_level = request.POST.get('log_level')

        cfg.set('config', 'ansible_path', a_path)
        cfg.set('config', 'project_base_path', pro_path)
        cfg.set('config', 'git_base_path', git_path)
        cfg.set('db', 'engine', engine)
        cfg.set('db', 'host', host)
        cfg.set('db', 'port', port)
        cfg.set('db', 'user', user)
        cfg.set('db', 'password', password)
        cfg.set('db', 'database', database)
        cfg.set('token', 'token', token)
        cfg.set('log', 'log_path', log_path)
        cfg.set('log', 'log_level', log_level)
        fp = open(configfile, 'w')
        cfg.write(fp)
        fp.close()
        tips = "保存成功！"
        display_control = ""
    else:

        engine = cfg.get('db', 'engine')
        host = cfg.get('db', 'host')
        port = cfg.get('db', 'port')
        user = cfg.get('db', 'user')
        password = cfg.get('db', 'password')
        database = cfg.get('db', 'database')

        log_path = cfg.get('log', 'log_path')
        log_level = cfg.get('log', 'log_level')
    return render(request,'skconfig/index.html', locals())


def get_dir(args):
    config = configparser.RawConfigParser()
#     dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(configfile, 'r') as cfgfile:
        config.readfp(cfgfile)
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')
        a_path = config.get('config', 'ansible_path')

 

    if args == "log_path":
        return log_path
    if args == "log_level":
        return log_level
    if args == "a_path":
        return a_path



def get_token(request):
    if request.method == 'POST':
        new_token = get_user_model().objects.make_random_password(length=12,
                                                                  allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
        return HttpResponse(new_token)
    else:
        return True


def get_ansible_config(args):
    config = configparser.RawConfigParser()
    dirs = get_dir("a_path")
    with open(dirs + '/ansible.cfg', 'r') as cfgfile:
        config.readfp(cfgfile)
        inventory = config.get('defaults', 'inventory')

    if args == "inventory":
        return inventory
def flower(request):
    flower_url = settings.FLOWER_URL
    #print(flower_url)
    return render(request, "skconfig/flower.html", {'flower_url':flower_url},locals())