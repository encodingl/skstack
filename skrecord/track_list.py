#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import Record_form
from .forms import Record_list_form
from .forms import Track_list_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.urls import reverse
from .models import Record
from .models import Record_list
from .models import Track_list


@login_required()
@permission_verify()
def track_list(request):
    temp_name = "skrecord/navi-header.html"
    track_list_info = Track_list.objects.all()
#    allnavi = navi.objects.all()
    return render(request,"skrecord/track_list.html", locals())

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        track_list_form = Track_list_form(request.POST)

        if track_list_form.is_valid():
            track_list_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render(request,"skrecord/track_list_add.html", locals())
    else:
        display_control = "none"
        track_list_form = Track_list_form()

        return render(request,"skrecord/track_list_add.html", locals())



@login_required
@permission_verify()
def track_list_delete(request, ids):
    Track_list.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('track_list'))

@login_required()
@permission_verify()
def message(request):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print("p_type value:%s" % P_type)
    if P_type:
        allnavi = Track_list.objects.filter(P_status=P_type)
    else:
        allnavi = Track_list.objects.all()
    print("the allnavi is %s" % allnavi);
    return render(request,"skrecord/track_list.html", locals())




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Track_list.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        track_list_form = Track_list_form(request.POST,instance=obj)
        if track_list_form.is_valid():
            track_list_form.save()
            return HttpResponseRedirect(reverse('track_list'))
    else:
        track_list_form = Track_list_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/track_list_edit.html', locals())


@login_required()
@permission_verify()
def detail(request,ids):
    obj = Track_list.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        track_list_form = Track_list_form(request.POST,instance=obj)
        if track_list_form.is_valid():
            track_list_form.save()
            return HttpResponseRedirect(reverse('track_list'))
    else:
        track_list_form = Track_list_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/track_list_detail.html', locals())




