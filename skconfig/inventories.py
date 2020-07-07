'''
Created on 2020年6月17日

@author: admin
'''
#! /usr/bin/env python
# -*- coding: utf-8 -*-


from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from lib.setup import get_AnsibleHostsDic,get_hostsFile
from django.shortcuts import render




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
        
        
    return render(request,'skconfig/inventories_index.html', locals())