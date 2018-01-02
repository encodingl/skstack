#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, RequestContext
from models import navi, WhiteList
from forms import WhiteList_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify


@login_required()
@permission_verify()
def whitelist(request):
    temp_name = "skdomain/navi-header.html"
    allwhitelist = WhiteList.objects.all()
    return render_to_response('skdomain/whitelist.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def whitelist_add(request):
    temp_name = "skdomain/navi-header.html"
    if request.method == "POST":
        whitelist_form = WhiteList_form(request.POST)
        if whitelist_form.is_valid():
            whitelist_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdomain/whitelist_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        whitelist_form = WhiteList_form()
        return render_to_response("skdomain/whitelist_add.html", locals(), RequestContext(request))


# @login_required()
# @permission_verify()
# def whitelist_add_mini(request):
#     temp_name = "skdomain/navi-header.html"
#     if request.method == "POST":
#         whitelist_form = WhiteList_form(request.POST)
#         if whitelist_form.is_valid():
#             whitelist_form.save()
#             tips = u"增加成功！"
#             display_control = ""
#             status = 1
#         else:
#             tips = u"增加失败！"
#             display_control = ""
#         return render_to_response("skdomain/whitelist_add_mini.html", locals(), RequestContext(request))
#     else:
#         display_control = "none"
#         whitelist_form = WhiteList_form()
#         return render_to_response("skdomain/whitelist_add_mini.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def whitelist_del(request):
    temp_name = "skdomain/navi-header.html"
    if request.method == 'POST':
        whitelist_items = request.POST.getlist('whitelist_check', [])
        if whitelist_items:
            for n in whitelist_items:
                WhiteList.objects.filter(id=n).delete()
    allwhitelist = WhiteList.objects.all()
    return render_to_response("skdomain/whitelist.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def whitelist_edit(request, ids):
    obj = WhiteList.objects.get(id=ids)
    allwhitelist = WhiteList.objects.all()
    return render_to_response("skdomain/whitelist_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def whitelist_save(request):
    temp_name = "skdomain/navi-header.html"
    if request.method == 'POST':
        whitelist_id = request.POST.get('id')
        ip = request.POST.get('ip')
        desc = request.POST.get('desc')
        whitelist_item = WhiteList.objects.get(id=whitelist_id)
        whitelist_item.ip = ip
        whitelist_item.desc = desc
        whitelist_item.save()
        obj = whitelist_item
        status = 1
    else:
        status = 2
    return render_to_response("skdomain/whitelist_edit.html", locals(), RequestContext(request))
