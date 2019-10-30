#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from skyw.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.template import RequestContext
from .forms import devopsform,rotaform,noticeform
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
# Create your views here.

@login_required()
@permission_verify()
def notify(request):
    temp_name = "skyw/yw-header.html"
    # person = Devops.objects.all()
    # rota = Rota.objects.all()
    notice = Notice.objects.all()
    # events = event.objects.all()
    # platform =  Platform.objects.all()
    # platformclasss=PlatFormclass.objects.all()
    # for yw in person:
    #    name = yw.name
    #    iphone = yw.iphone
    return render(request,"skyw/ywnotify.html", locals())



@login_required()
@permission_verify()
def notice_add(request):
    temp_name = "skyw/yw-header.html"
    if request.method == "POST":
       notice=noticeform(request.POST)
       if notice.is_valid():
           notice.save()
           tips = '增加成功'
           display_control = ""
       else:
           tips = "增加失败"
           display_control = ""
    else:
        display_control = "none"
        notice = noticeform()
    return render(request,"skyw/notice_add.html",locals(),RequestContext(request))

@login_required()
@permission_verify()
def notice_delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    Notice.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('notify'))
def str2gb(args):
    return str(args).encode('gb2312')
@login_required()
@permission_verify()
def notice_edit(request,ids):
    obj = Notice.objects.get(id=ids)
    temp_name = "skyw/yw-header.html"
    if request.method=="POST":
        notice_form = noticeform(request.POST,instance=obj)
        if notice_form.is_valid():
            notice_form.save()
            tips="编辑成功"
        else:
            tips = "编辑失败"
            display_control = ""
      #      return HttpResponseRedirect(reverse('notice_edit'))
    else:
        display_control = "none"
        notice_form= noticeform(instance=obj)
    return render(request,'skyw/notice_edit.html',locals(),RequestContext(request))
