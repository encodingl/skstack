#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

def url_permission(request):
    url_permission_list = []
    permission_flag = False
    if request.user.is_superuser:
        permission_flag = True
    elif request.user.username and request.user.role:
        url_permission = request.user.role.permission.values_list('url')
        url_permission_list = [u[0] for u in url_permission if not u[0].startswith('/')]
        if 'show_all_menu' in url_permission_list:
            permission_flag = True
    url_permission_list=json.dumps(url_permission_list)
    return {'url_permission_list': url_permission_list, 'permission_flag': permission_flag}