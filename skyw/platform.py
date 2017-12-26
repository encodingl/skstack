#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from skyw.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect,RequestContext
from forms import *
from django.core.urlresolvers import reverse
import json
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify,permission_verify_ids
# Create your views here.

@login_required()
@permission_verify()
def platformclass_add(request, *args, **kwargs):
    temp_name = "skyw/yw-header.html"
    if request.method == "POST":
       platformclasss =  platformclassform(request.POST)
       if platformclasss.is_valid():

           platformclasss.save()
           tips = u'增加成功'
           display_control=" "
       else:
           tips = u"增加失败"
           display_control = ""
    else:
        display_control = "none"
        platformclasss = platformclassform()
    return render_to_response("skyw/platformclass_add.html", locals(), RequestContext(request))
@login_required()
@permission_verify()
def platformclass_delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    PlatFormclass.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('list'))
@login_required()
@permission_verify()
def platformclass_edit(request,ids):
    temp_name = "skyw/yw-header.html"
    platformclassedit = PlatFormclass.objects.get(id=ids)
    if request.method=="POST":
        platformclassforms = platformclassform(request.POST,instance=platformclassedit)
        if platformclassforms.is_valid():
            platformclassforms.save()
            tips=u"编辑成功"
            display_control=" "
        else:
            tips=u"编辑失败"
            display_control=" "
    else:
        display_control = "none"
        platformclassforms= platformclassform(instance=platformclassedit)
    return render_to_response('skyw/platformclass_edit.html',locals(),RequestContext(request))
@login_required()
@permission_verify()
def platform_add(request, *args, **kwargs):
    temp_name = "skyw/yw-header.html"
    if request.method == "POST":
       platform = platformform(request.POST)
       if platform.is_valid() :
           platform.save()
           tips = u'增加成功'
           display_control=" "
       else:
           tips = u"增加失败"
           display_control = ""
    else:
        display_control = "none"
        platform = platformform()
    return render_to_response("skyw/platform_add.html", locals(), RequestContext(request))
@login_required()
@permission_verify()
def platform_delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    Platform.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('list'))
def str2gb(args):
    return str(args).encode('gb2312')
@login_required()
@permission_verify()
def platform_edit(request,ids):
    platformedit = Platform.objects.get(id=ids)
    temp_name = "skyw/yw-header.html"
    if request.method=="POST":
        nform = platformform(request.POST,instance=platformedit)
        if nform.is_valid():
            nform.save()
            tips = u"编辑成功"
            display_control=" "
        else:
            tips="编辑失败"
            display_control=" "
    else:
        display_control = "none"
        nform= platformform(instance=platformedit)
    return render_to_response('skyw/platform_edit.html',locals(),RequestContext(request))



