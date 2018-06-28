#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from skyw.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect,RequestContext
from forms import devopsform,rotaform,noticeform,eventform
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
# Create your views here.

@login_required()
@permission_verify()
def ywevent(request):
    temp_name = "skyw/yw-header.html"
    # person = Devops.objects.all()
    # rota = Rota.objects.all()
    # notice = Notice.objects.all()
    events = event.objects.all()
    # platform =  Platform.objects.all()
    # platformclasss=PlatFormclass.objects.all()
    # for yw in person:
    #    name = yw.name
    #    iphone = yw.iphone
    return render_to_response("skyw/ywevent.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def event_add(request):
    temp_name = "skyw/yw-header.html"
    if request.method == "POST":
       events = eventform(request.POST)
       if events.is_valid(): 
           events.save()
           tips = u'增加成功'
           display_control = ""
          # return HttpResponseRedirect(reverse('yw'))
       else:
           tips = u"增加失败"
           display_control = ""
    else:
        display_control = "none"
        events = eventform()
    return render_to_response("skyw/event_add.html", locals(), RequestContext(request))
@login_required()
@permission_verify()
def event_delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    event.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('list'))
def str2gb(args):
    return str(args).encode('gb2312')
@login_required()
@permission_verify()
def event_edit(request,ids):
    events_edit = event.objects.get(id=ids)
    temp_name = "skyw/yw-header.html"
    if request.method=="POST":
        event_form = eventform(request.POST,instance=events_edit)
        if event_form.is_valid():
            event_form.save()
            tips = u"编辑成功"
            display_control=""
        else:
            tips=u"编辑成功"
            display_control=""
    else:
        display_control = "none"
        event_form= eventform(instance=events_edit)
    return render_to_response('skyw/event_edit.html',locals(),RequestContext(request))



