#! /usr/bin/env python
# -*- coding: utf-8 -*-


from .models import AuditFlow

from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify


from .forms import AuditFlow_form
from django.shortcuts import render
from django.template import RequestContext
from skcmdb.api import get_object

import logging
log = logging.getLogger('skworkorders')


@login_required()
@permission_verify()
def AuditFlow_index(request):
    temp_name = "skaccounts/accounts-header.html"    
    tpl_all = AuditFlow.objects.all()
    
    return render(request,'skaccounts/AuditFlow_index.html', locals())

@login_required()
@permission_verify()
def AuditFlow_add(request):
    temp_name = "skaccounts/accounts-header.html"
    if request.method == "POST":
        tpl_AuditFlow_form = AuditFlow_form(request.POST)
        if tpl_AuditFlow_form.is_valid():
            tpl_AuditFlow_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render(request,"skaccounts/AuditFlow_add.html", locals())
    else:
        display_control = "none"
        tpl_AuditFlow_form = AuditFlow_form()
        return render(request,"skaccounts/AuditFlow_add.html", locals())



@login_required()
@permission_verify()
def AuditFlow_del(request):
    temp_name = "skaccounts/accounts-header.html"
    obj_id = request.GET.get('id', '')  
    if obj_id:
        try:
            AuditFlow.objects.filter(id=obj_id).delete()
        except Exception as tpl_error_msg:
            log.warning(tpl_error_msg)
        tpl_all = AuditFlow.objects.all()
        return render(request,"skaccounts/AuditFlow_index.html", locals())


@login_required()
@permission_verify()
def AuditFlow_edit(request, ids):
    status = 0
    obj = get_object(AuditFlow, id=ids)
    
    if request.method == 'POST':
        tpl_AuditFlow_form = AuditFlow_form(request.POST, instance=obj)
        if tpl_AuditFlow_form.is_valid():
            tpl_AuditFlow_form.save()
            status = 1
        else:
            status = 2
    else:
        tpl_AuditFlow_form = AuditFlow_form(instance=obj)      
    return render(request,"skaccounts/AuditFlow_edit.html", locals())
