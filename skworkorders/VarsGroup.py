#! /usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponse
from .models import VarsGroup
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify


from .forms import VarsGroup_form
from django.shortcuts import render_to_response
from django.template import RequestContext
from skcmdb.api import get_object

import time
import logging
log = logging.getLogger('skstack')



@login_required()
@permission_verify()
def VarsGroup_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = VarsGroup.objects.all()
    print(tpl_all)
    return render_to_response('skworkorders/VarsGroup_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def VarsGroup_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_VarsGroup_form = VarsGroup_form(request.POST)
        if tpl_VarsGroup_form.is_valid():
            tpl_VarsGroup_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render_to_response("skworkorders/VarsGroup_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_VarsGroup_form = VarsGroup_form()
        return render_to_response("skworkorders/VarsGroup_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def VarsGroup_del(request):
    temp_name = "skworkorders/skworkorders-header.html"
    obj_id = request.GET.get('id', '')  
    if obj_id:
        try:
            VarsGroup.objects.filter(id=obj_id).delete()
        except Exception as tpl_error_msg:
            log.warning(tpl_error_msg)
        tpl_all = VarsGroup.objects.all()
        return render_to_response("skworkorders/VarsGroup_index.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def VarsGroup_copy(request):
    temp_name = "skworkorders/skworkorders-header.html"
    Vars_id = request.GET.get('id', '')
    if Vars_id:
        obj = VarsGroup.objects.get(id=Vars_id)
        obj.pk=None
        obj.name = obj.name + "_copy_" + time.strftime("%H%M%S", time.localtime()) 
        obj.save()  
    tpl_all = VarsGroup.objects.all()
    return render_to_response('skworkorders/VarsGroup_index.html', locals(), RequestContext(request))




@login_required()
@permission_verify()
def VarsGroup_edit(request, ids):
    temp_name = "skworkorders/skworkorders-header.html"
    obj = get_object(VarsGroup, id=ids)
    
    if request.method == 'POST':
        tpl_VarsGroup_form = VarsGroup_form(request.POST, instance=obj)
        if tpl_VarsGroup_form.is_valid():
            tpl_VarsGroup_form.save()
            tips = "保存成功！"
            display_control = ""
        else:
            tips = "保存失败！"
            display_control = ""
    else:
        display_control = "none"
        tpl_VarsGroup_form = VarsGroup_form(instance=obj)      
    return render_to_response("skworkorders/VarsGroup_edit.html", locals(), RequestContext(request))
