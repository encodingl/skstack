#!/usr/bin/env python
# -*- coding: utf-8 -*-

def url_permission(request):
    url_permission_list = []
    permission_flag = False
    if request.user.username and request.user.role:
        url_permission = request.user.role.permission.values_list('url')
        url_permission_list = [u[0] for u in url_permission]
        if '/' in url_permission_list:
            permission_flag = True
    elif request.user.is_superuser:
        permission_flag = True
    return {'url_permission_list': url_permission_list, 'permission_flag': permission_flag}
