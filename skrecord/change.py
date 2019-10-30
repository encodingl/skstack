#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import Record_form
from .forms import Faq_form
from .forms import Change_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.urls import reverse
from .models import Record
from .models import Faq
from .models import Change


@login_required()
@permission_verify()
def change(request):
    temp_name = "skrecord/navi-header.html"
    change_info = Change.objects.all()
#    allnavi = navi.objects.all()
    return render(request,"skrecord/change.html", locals())

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        change_form = Change_form(request.POST)

        if change_form.is_valid():
            change_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render(request,"skrecord/change_add.html", locals())
    else:
        display_control = "none"
        change_form = Change_form()

        return render(request,"skrecord/change_add.html", locals())



@login_required
@permission_verify()
def change_delete(request, ids):
    Change.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('change'))

@login_required()
@permission_verify()
def message(request):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print("p_type value:%s" % P_type)
    if P_type:
        allnavi = Change.objects.filter(P_status=P_type)
    else:
        allnavi = Change.objects.all()
    print("the allnavi is %s" % allnavi);
    return render(request,"skrecord/change.html", locals())




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Change.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        change_form = Change_form(request.POST,instance=obj)
        if change_form.is_valid():
            change_form.save()
            return HttpResponseRedirect(reverse('change'))
    else:
        change_form = Change_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/change_edit.html', locals())


@login_required()
@permission_verify()
def detail(request,ids):
    obj = Change.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        change_form = Change_form(request.POST,instance=obj)
        if change_form.is_valid():
            change_form.save()
            return HttpResponseRedirect(reverse('change'))
    else:
        change_form = Change_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/change_detail.html', locals())



