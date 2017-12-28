#!/usr/bin/env python
# -*- coding: utf-8 -*-

def url_permission(request):
    if not request.user.is_superuser:
        url_permission = request.user.role.permission.values_list('name')
        url_permission_list = [u[0] for u in url_permission]
    else:
        url_permission_list  = ['/all']
    return {'url_permission_list': url_permission_list}

