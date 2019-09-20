#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from skyw.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.template import RequestContext
from .forms import devopsform,rotaform
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
# Create your views here.

@login_required()
@permission_verify()
def dutyinfo(request):
    temp_name = "skyw/yw-header.html"
    # person = Devops.objects.all()
    rota = Rota.objects.all()
    # notice = Notice.objects.all()
    # events = event.objects.all()
    # platform =  Platform.objects.all()
    # platformclasss=PlatFormclass.objects.all()
    # for yw in person:
    #    name = yw.name
    #    iphone = yw.iphone
    return render(request,"skyw/dutyinfo.html", locals())

@login_required()
@permission_verify()
def rota_add(request):
    temp_name = "skyw/yw-header.html"
    if request.method == "POST":
       rota=rotaform(request.POST)
       #print(rota.cleaned_data)
       if rota.is_valid():
           #print(rota.cleaned_data)
           print('success')
           rota.save()
           tips = '增加成功'
           display_control = ""
       else:
           #rota.save()
           print('test')
           print((rota.cleaned_data['iphone']))
           print((rota.cleaned_data['name']))
           print((rota.cleaned_data['spell']))
           # print(rota.cleaned_data['rota_number'])
           print((rota.cleaned_data['emergency_contact']))
           print((rota.cleaned_data['iphone_rota']))
           tips = "增加失败"
           displ_control = ""
    else:
        display_control = "none"
        rota = rotaform()
    return render(request,"skyw/rota_add.html",locals(),RequestContext(request))

@login_required()
@permission_verify()
def rota_delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    Rota.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('dutyinfo'))
def str2gb(args):
    return str(args).encode('gb2312')
@login_required()
@permission_verify()
def rota_edit(request,ids):
    temp_name = "skyw/yw-header.html"
    rota_edit = Rota.objects.get(id=ids)
    if request.method=="POST":
        rota_form = rotaform(request.POST,instance=rota_edit)
        if rota_form.is_valid():
            rota_form.save()
            tips = "编辑成功！"
            display_control = ""
        else:
            tips = "编辑失败！"
            display_control = ""
    else:
        display_control = "none"
        rota_form= rotaform(instance=rota_edit)
    return render(request,'skyw/rota_edit.html',locals(),RequestContext(request))
