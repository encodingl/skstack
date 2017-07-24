#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import job,job,extravars
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log
from lib.setup import get_playbook, get_roles,get_AnsibleHostsDic,get_hostsFile
from .models import history
from .forms import Job_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
# var info



ansible_dir = get_dir("a_path")


@login_required()
@permission_verify()
def index(request):
    temp_name = "sktask/setup-header.html"
    list_hostsFile = get_hostsFile(ansible_dir)
    
    dic_dic_groups={}
    dic_list_key={}
    for h in list_hostsFile:
    
       
        all_ansible_groups,list_key,list_key_gp = get_AnsibleHostsDic(ansible_dir+h)
        dic_dic_groups[h]=all_ansible_groups
        dic_list_key[h]=list_key
          
        
    return render_to_response('sktask/inventories_index.html', locals(), RequestContext(request))



