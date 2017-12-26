#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from models import UserGroup
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify,permission_verify_ids
import logging
from lib.log import log
from .forms import UserGroup_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import json
import logging
from billiard.util import INFO
import sys
from datetime import datetime
from django.core.urlresolvers import reverse



@login_required()
@permission_verify()
def UserGroup_index(request, *args, **kwargs):
    temp_name = "skaccounts/accounts-header.html"    
    tpl_all = UserGroup.objects.all()
    return render_to_response('skaccounts/UserGroup_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def UserGroup_add(request, *args, **kwargs):
    temp_name = "skaccounts/accounts-header.html"
    if request.method == "POST":
        tpl_UserGroup_form = UserGroup_form(request.POST)
        if tpl_UserGroup_form.is_valid():
            tpl_UserGroup_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skaccounts/UserGroup_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_UserGroup_form = UserGroup_form()
        return render_to_response("skaccounts/UserGroup_add.html", locals(), RequestContext(request))



@login_required()
@permission_verify()
def UserGroup_del(request, *args, **kwargs):
#    temp_name = "skaccounts/accounts-header.html"
    UserGroup_id = request.GET.get('id', '')
    if UserGroup_id:
        UserGroup.objects.filter(id=UserGroup_id).delete()
    
    if request.method == 'POST':
        UserGroup_items = request.POST.getlist('x_check', [])
        if UserGroup_items:
            for n in UserGroup_items:
                UserGroup.objects.filter(id=n).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify_ids()
def UserGroup_edit(request, ids):
    temp_name = "skaccounts/accounts-header.html"
    status = 0
    obj = get_object(UserGroup, id=ids)
    
    if request.method == 'POST':
        tpl_UserGroup_form = UserGroup_form(request.POST, instance=obj)
        if tpl_UserGroup_form.is_valid():
            tpl_UserGroup_form.save()
            status = 1
            return HttpResponseRedirect(reverse('UserGroup_index'))
        else:
            status = 3
    else:
        tpl_UserGroup_form = UserGroup_form(instance=obj)      
    return render_to_response("skaccounts/UserGroup_edit.html", locals(), RequestContext(request))




    