#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Vars 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from .forms import Vars_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object
import time
from skworkorders.lib_skworkorders import get_Vars_form




@login_required()
@permission_verify()
def Vars_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = Vars.objects.all()
    
    return render_to_response('skworkorders/Vars_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def Vars_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_Vars_form = Vars_form(request.POST)
        if tpl_Vars_form.is_valid():
            tpl_Vars_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render_to_response("skworkorders/Vars_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_Vars_form = Vars_form()
        return render_to_response("skworkorders/Vars_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def Vars_del(request):
#    temp_name = "skworkorders/skworkorders-header.html"
    Vars_id = request.GET.get('id', '')
    if Vars_id:
        Vars.objects.filter(id=Vars_id).delete()
    
    if request.method == 'POST':
        Vars_items = request.POST.getlist('x_check', [])
        if Vars_items:
            for n in Vars_items:
                Vars.objects.filter(id=n).delete()
    return HttpResponse('删除成功')

@login_required()
@permission_verify()
def Vars_copy(request):
    temp_name = "skworkorders/skworkorders-header.html"
    Vars_id = request.GET.get('id', '')
    if Vars_id:
        obj = Vars.objects.get(id=Vars_id)
        obj.pk=None
        obj.name = obj.name + "_copy_" + time.strftime("%H%M%S", time.localtime()) 
        obj.save()  
    tpl_all = Vars.objects.all()
    return render_to_response('skworkorders/Vars_index.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def Vars_edit(request, ids):
    status = 0
    obj = get_object(Vars, id=ids)
    
    if request.method == 'POST':
        tpl_Vars_form = Vars_form(request.POST, instance=obj)
        if tpl_Vars_form.is_valid():
            tpl_Vars_form.save()
            status = 1
            tips = "successful！"
            display_control = ""
        else:
            tips = "failed！"
            display_control = ""
    else:
        display_control = "none"
        tpl_Vars_form = Vars_form(instance=obj)      
    return render_to_response("skworkorders/Vars_edit2.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def Vars_check(request,ids):
    temp_name = "skworkorders/skworkorders-header.html"
    obj = get_object(Vars, id=ids)
    tpl_var_check_form = get_Vars_form(obj)
    return render_to_response("skworkorders/Vars_check.html", locals(), RequestContext(request))
