#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import Record_form
from .forms import Faq_form
from .forms import Assessment_form
from .forms import Assessment_list_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.urls import reverse
from .models import Record
from .models import Faq
from .models import Assessment
from .models import Assessment_list


@login_required()
@permission_verify()
def assessment_list(request):
    temp_name = "skrecord/navi-header.html"
    assessment_list_info = Assessment_list.objects.all()
#    allnavi = navi.objects.all()
    return render(request,"skrecord/assessment_list.html", locals())

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        assessment_list_form = Assessment_list_form(request.POST)

        if assessment_list_form.is_valid():
            assessment_list_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render(request,"skrecord/assessment_list_add.html", locals())
    else:
        display_control = "none"
        assessment_list_form = Assessment_list_form()

        return render(request,"skrecord/assessment_list_add.html", locals())



@login_required
@permission_verify()
def assessment_list_delete(request, ids):
    Assessment_list.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('assessment_list'))

@login_required()
@permission_verify()
def message(request):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print("p_type value:%s" % P_type)
    if P_type:
        allnavi = Assessment_list.objects.filter(P_status=P_type)
    else:
        allnavi = Assessment_list.objects.all()
    print("the allnavi is %s" % allnavi);
    return render(request,"skrecord/assessment_list.html", locals())




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Assessment_list.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        assessment_list_form = Assessment_list_form(request.POST,instance=obj)
        if assessment_list_form.is_valid():
            assessment_list_form.save()
            return HttpResponseRedirect(reverse('assessment_list'))
    else:
        assessment_list_form = Assessment_list_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/assessment_list_edit.html', locals())

@login_required()
@permission_verify()
def detail(request,ids):
    obj = Assessment_list.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        assessment_list_form = Assessment_list_form(request.POST,instance=obj)
        if assessment_list_form.is_valid():
            assessment_list_form.save()
            return HttpResponseRedirect(reverse('assessment_list'))
    else:
        assessment_list_form = Assessment_list_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/assessment_list_detail.html', locals())




