

#! /usr/bin/env python
# -*- coding: utf-8 -*-
def audit_cmd(*args):
    login_user=request.user
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    
    his=history(login_user=login_user,src_ip=ip,cmd=cmd,cmd_result=cmd_result)
    his.save()