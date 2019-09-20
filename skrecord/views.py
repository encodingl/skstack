#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import Record_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.urls import reverse
from .models import Record


@login_required()
@permission_verify()
def index(request):
    temp_name = "skrecord/navi-header.html"
    record_info = Record.objects.all()
#    allnavi = navi.objects.all()
    return render(request,"skrecord/index.html", locals())

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        record_form = Record_form(request.POST)

        if record_form.is_valid():
            record_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render(request,"skrecord/record_add.html", locals())
    else:
        display_control = "none"
        record_form = Record_form()

        return render(request,"skrecord/record_add.html", locals())



@login_required
@permission_verify()
def delete(request, ids):
    Record.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('record'))

@login_required()
@permission_verify()
def message(request, EVENT_STATUS=None):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print("p_type value:%s" % P_type)
    if P_type:
        allnavi = Record.objects.filter(P_status=P_type)
    else:
        allnavi = Record.objects.all()
    print("the allnavi is %s" % allnavi);
    return render(request,"skrecord/record.html", locals())




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Record.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        record_form = Record_form(request.POST,instance=obj)
        if record_form.is_valid():
            record_form.save()
            return HttpResponseRedirect(reverse('record'))
    else:
        record_form = Record_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/record_edit.html', locals())


@login_required()
@permission_verify()
def detail(request,ids):
    obj = Record.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        record_form = Record_form(request.POST,instance=obj)
        if record_form.is_valid():
            record_form.save()
            return HttpResponseRedirect(reverse('record'))
    else:
        record_form = Record_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/record_detail.html', locals())




