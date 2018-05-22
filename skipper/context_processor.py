#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from skaccounts.models import UserInfo, RoleList, PermissionList

def url_permission(request):
    url_permission_list=[]
    if request.user.is_superuser:
        url_permission_list=['/all/']
        return {'url_permission_list': url_permission_list}
        
            
    elif request.user.username and request.user.role:
        iUser = UserInfo.objects.get(username=request.user)
        role_permission = RoleList.objects.get(name=iUser.role)
        role_permission_list = role_permission.permission.all()
        for l in role_permission_list:
            url_permission_list.append(str(l.url))
        
    return {'url_permission_list': url_permission_list}
  