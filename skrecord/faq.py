#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import Record_form
from .forms import Faq_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.urls import reverse
from .models import Record
from .models import Faq
from skaccounts.models import UserInfo
from django.db import models


@login_required()
@permission_verify()
def faq(request):
    temp_name = "skrecord/navi-header.html"
    faq_info = Faq.objects.all()
    #Faq.user = UserInfo.objects.get(username=request.user)
    #Faq.user = request.user
#    allnavi = navi.objects.all()
    return render(request,"skrecord/faq.html", locals())

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        faq_form = Faq_form(request.POST,request.FILES)
        if faq_form.is_valid():
            #Faq.user = UserInfo.objects.get(username=request.user)
            #user = Faq.user
            #user = Faq.objects.create(user = Faq.user)
            #faq_form.save()
            Faq.user = request.user
            title = faq_form.cleaned_data['title']
            problemclass = faq_form.cleaned_data['problemclass']
            describe = faq_form.cleaned_data['describe']
            solution = faq_form.cleaned_data['solution']
            user = Faq.objects.create(user=Faq.user, title=title, problemclass=problemclass, describe=describe, solution=solution)
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render(request,"skrecord/faq_add.html", locals())
    else:
        display_control = "none"
        faq_form = Faq_form()

        return render(request,"skrecord/faq_add.html", locals())



@login_required
@permission_verify()
def faq_delete(request, ids):
    Faq.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('faq'))

@login_required()
@permission_verify()
def message(request):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print("p_type value:%s" % P_type)
    if P_type:
        allnavi = Faq.objects.filter(P_status=P_type)
    else:
        allnavi = Faq.objects.all()
    print("the allnavi is %s" % allnavi);
    return render(request,"skrecord/faq.html", locals())




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Faq.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        faq_form = Faq_form(request.POST,instance=obj)
        if faq_form.is_valid():
            faq_form.save()
            return HttpResponseRedirect(reverse('faq'))
    else:
        faq_form = Faq_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/faq_edit.html', locals())


@login_required()
@permission_verify()
def detail(request,ids):
    obj = Faq.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        faq_form = Faq_form(request.POST,instance=obj)
        if faq_form.is_valid():
            faq_form.save()
            return HttpResponseRedirect(reverse('faq'))
    else:
        faq_form = Faq_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render(request,'skrecord/faq_detail.html', locals())

#@login_required()
#@permission_verify()
#def save_models(self):
#    Faq.objects.user = UserInfo.request.user
#    Faq().save_models()
#def save_models(request,ids):
#    obj = Faq.objects.get(id=ids)
#    faq.user = faq.request.user
#    faq().save_models()


