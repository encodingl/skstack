#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from skyw.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect,RequestContext
from forms import devopsform,rotaform
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
# Create your views here.
@login_required()
@permission_verify()
def rota_add(request):
    temp_name = "skyw/yw-header.html"
    rotadata = Rota.objects.all()
    dbadata = Devops.objects.all()
    for i in dbadata:
        job=i.job
        if job == 3:
            print i.name , i.iphone

    if request.method == "POST":
       rota=rotaform(request.POST)
       if rota.is_valid():
           rota.save()
           tips = u'增加成功'
           display_control = ""
       else:
           tips = u"增加失败"
           displ_control = ""
    else:
        rota = rotaform()
    return render_to_response("skyw/rota_add.html",locals(),RequestContext(request))

@login_required()
@permission_verify()
def rota_delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    Rota.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('list'))
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
            tips = u"编辑成功！"
            display_control = ""
        else:
            tips = u"编辑失败！"
            display_control = ""
    else:
        rota_form= rotaform(instance=rota_edit)
    return render_to_response('skyw/rota_edit.html',locals(),RequestContext(request))
