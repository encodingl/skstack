#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import Record_form
from .forms import Faq_form
from .forms import Change_form
from .forms import Memo_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from lib.com import config, cfg
from .models import Record
from .models import Faq
from .models import Change
from .models import Memo
import datetime
import time


@login_required()
@permission_verify()
def memo(request):
    temp_name = "skrecord/navi-header.html"
    memo_info = Memo.objects.all()
#    allnavi = navi.objects.all()
    return render(request,"skrecord/memo.html", locals())

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        memo_form = Memo_form(request.POST,request.FILES)
        if memo_form.is_valid():
            #memo_form.save()
            Memo.user = request.user
            title = memo_form.cleaned_data['title']
            content = memo_form.cleaned_data['content']
            mail = memo_form.cleaned_data['mail']
            noticetime = memo_form.cleaned_data['noticetime']
            expirationtime = memo_form.cleaned_data['expirationtime']
            MEMO = Memo.objects.create(user=Memo.user, title=title, content=content, mail=mail, noticetime=noticetime, expirationtime=expirationtime)
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render(request,"skrecord/memo_add.html", locals())
    else:
        display_control = "none"
        memo_form = Memo_form()

        return render(request,"skrecord/memo_add.html", locals())



@login_required
@permission_verify()
def memo_delete(request, ids):
    Memo.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('memo'))

@login_required()
@permission_verify()
def message(request):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print("p_type value:%s" % P_type)
    if P_type:
        allnavi = Memo.objects.filter(P_status=P_type)
    else:
        allnavi = Memo.objects.all()
    print("the allnavi is %s" % allnavi);
    return render(request,"skrecord/memo.html", locals())




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Memo.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        memo_form = Memo_form(request.POST,instance=obj)
        if memo_form.is_valid():
            memo_form.save()
            return HttpResponseRedirect(reverse('memo'))
    else:
        memo_form = Memo_form(instance=obj)

    return render(request,'skrecord/memo_edit.html', locals())


@login_required()
@permission_verify()
def detail(request,ids):
    obj = Memo.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        memo_form = Memo_form(request.POST,instance=obj)
        if memo_form.is_valid():
            memo_form.save()
            return HttpResponseRedirect(reverse('memo'))
    else:
        memo_form = Memo_form(instance=obj)

    return render(request,'skrecord/memo_detail.html', locals())
