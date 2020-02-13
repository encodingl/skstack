#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Environment
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from .forms import Environment_form
from django.shortcuts import render
from django.template import RequestContext
from lib.com import get_object
import logging
log = logging.getLogger('skworkorders')


@login_required()
@permission_verify()
def Environment_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = Environment.objects.all()
    
    return render(request,'skworkorders/Environment_index.html', locals())

@login_required()
@permission_verify()
def Environment_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_Environment_form = Environment_form(request.POST)
        if tpl_Environment_form.is_valid():     
            tpl_Environment_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render(request,"skworkorders/Environment_add.html", locals())
    else:
        display_control = "none"
        tpl_Environment_form = Environment_form()
        return render(request,"skworkorders/Environment_add.html", locals())





@login_required()
@permission_verify()
def Environment_del(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    obj_id = request.GET.get('id', '')  
    if obj_id:
        try:
            Environment.objects.filter(id=obj_id).delete()
        except Exception as tpl_error_msg:
            log.warning(tpl_error_msg)
        tpl_all = Environment.objects.all()
        return render(request,"skworkorders/Environment_index.html", locals())


@login_required()
@permission_verify()
def Environment_edit(request, ids):
    status = 0
    obj = get_object(Environment, id=ids)
    
    if request.method == 'POST':
        tpl_Environment_form = Environment_form(request.POST, instance=obj)
        if tpl_Environment_form.is_valid():

            tpl_Environment_form.save()
            status = 1
        else:
            status = 2
    else:
        tpl_Environment_form = Environment_form(instance=obj)      
    return render(request,"skworkorders/Environment_edit.html", locals())




    