#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from .models import UserGroup

from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify

from .forms import UserGroup_form
from django.shortcuts import render_to_response
from django.template import RequestContext
from skcmdb.api import get_object

from django.core.urlresolvers import reverse
import logging
log = logging.getLogger('skstack')



@login_required()
@permission_verify()
def UserGroup_index(request):
    temp_name = "skaccounts/accounts-header.html"    
    tpl_all = UserGroup.objects.all()
    return render_to_response('skaccounts/UserGroup_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def UserGroup_add(request):
    temp_name = "skaccounts/accounts-header.html"
    if request.method == "POST":
        tpl_UserGroup_form = UserGroup_form(request.POST)
        if tpl_UserGroup_form.is_valid():
            tpl_UserGroup_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render_to_response("skaccounts/UserGroup_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_UserGroup_form = UserGroup_form()
        return render_to_response("skaccounts/UserGroup_add.html", locals(), RequestContext(request))



@login_required()
@permission_verify()
def UserGroup_del(request):
    temp_name = "skaccounts/accounts-header.html"
    obj_id = request.GET.get('id', '')  
    if obj_id:
        try:
            UserGroup.objects.filter(id=obj_id).delete()
        except Exception as tpl_error_msg:
            log.warning(tpl_error_msg)
        tpl_all = UserGroup.objects.all()
        return render_to_response("skaccounts/UserGroup_index.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
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




    