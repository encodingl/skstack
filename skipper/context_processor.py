#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from skaccounts.models import UserInfo, RoleList, PermissionList
from skworkorders.models import *
from django.db.models import Q
from django.db.models import Count

def url_permission(request):
    url_permission_list=[]
    if request.user.is_superuser:
        url_permission_list=['/all/']
   
    elif request.user.username and request.user.role:
        iUser = UserInfo.objects.get(username=request.user)
        role_permission = RoleList.objects.get(name=iUser.role)
        role_permission_list = role_permission.permission.all()
        for l in role_permission_list:
            url_permission_list.append(str(l.url))
        
    return {'url_permission_list': url_permission_list}

def skworkorder_todo_statistics(request):
    if request.user:
        
        obj_audit_count = WorkOrderFlow.objects.filter(status__in=[1,2,5,6,7,8]).aggregate(num=Count(id))
        tpl_unfinished_workorders=obj_audit_count["num"]
    
    return {'tpl_unfinished_workorders': tpl_unfinished_workorders}
  