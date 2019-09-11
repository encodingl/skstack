#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Environment
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from .forms import Environment_form
from django.shortcuts import render_to_response
from django.template import RequestContext
from skcmdb.api import get_object
import logging
log = logging.getLogger('skworkorders')


@login_required()
@permission_verify()
def Environment_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = Environment.objects.all()
    
    return render_to_response('skworkorders/Environment_index.html', locals(), RequestContext(request))

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
        return render_to_response("skworkorders/Environment_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_Environment_form = Environment_form()
        return render_to_response("skworkorders/Environment_add.html", locals(), RequestContext(request))





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
        return render_to_response("skworkorders/Environment_index.html", locals(), RequestContext(request))


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
    return render_to_response("skworkorders/Environment_edit.html", locals(), RequestContext(request))




    