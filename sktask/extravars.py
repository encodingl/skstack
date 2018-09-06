#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from django.shortcuts import render
from django.http import HttpResponse
from models import extravars
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log
from lib.setup import get_playbook, get_roles
from .forms import Extravars_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object

# var info

proj_base_dir = get_dir("pro_path")



@login_required()
@permission_verify()
def extravars_index(request):
    temp_name = "sktask/setup-header.html"
    allextravars = extravars.objects.all()
    return render_to_response('sktask/extravars_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def extravars_add(request):
    temp_name = "sktask/setup-header.html"
    if request.method == "POST":
        extravars_form = Extravars_form(request.POST)
        if extravars_form.is_valid():
            extravars_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("sktask/extravars_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        extravars_form = Extravars_form()
        return render_to_response("sktask/extravars_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def extravars_del(request):
    temp_name = "sktask/setup-header.html"
    extravars_id = request.GET.get('id', '')
    if extravars_id:
        extravars.objects.filter(id=extravars_id).delete()
    if request.method == 'POST':
        extravars_items = request.POST.getlist('check_box', [])
        if extravars_items:
            for n in extravars_items:
                extravars.objects.filter(id=n).delete()
    allextravars = extravars.objects.all()
    return render_to_response("sktask/extravars_index.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
# def extravars_edit(request, ids):
#     obj = extravars.objects.get(id=ids)
#     allextravars = extravars.objects.all()
#     return render_to_response("sktask/extravars_edit.html", locals(), RequestContext(request))

def extravars_edit(request, ids):
    status = 0
#     asset_types = online_status
    obj = get_object(extravars, id=ids)
#     obj = extravars.objects.get(id=ids)
    if request.method == 'POST':
        obj_f = Extravars_form(request.POST, instance=obj)
        if obj_f.is_valid():
            obj_f.save()
            status = 1
        else:
            status = 2
    else:
        obj_f = Extravars_form(instance=obj)      
    return render_to_response("sktask/extravars_edit.html", locals(), RequestContext(request))

