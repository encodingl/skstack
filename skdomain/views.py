#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import navi, NAVI_STATUS
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, RequestContext
from forms import navi_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.core.urlresolvers import reverse


@login_required()
@permission_verify()
def index(request):
    temp_name = "skdomain/navi-header.html"
    allnavi = navi.objects.all()
    return render_to_response("skdomain/index.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def add(request):
    temp_name = "skdomain/navi-header.html"
    if request.method == "POST":
        n_form = navi_form(request.POST)
        if n_form.is_valid():
            n_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skdomain/add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        n_form = navi_form()
        
        return render_to_response("skdomain/add.html", locals(), RequestContext(request))



@login_required
@permission_verify()
def delete(request, ids):
    navi.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('manage'))

@login_required()
@permission_verify()
def manage(request):
    temp_name = "skdomain/navi-header.html"
    
    online_status = NAVI_STATUS
    online_type = request.GET.get('online_type', '')
    print "online_type value:%s" % online_type
    if online_type:
        allnavi = navi.objects.filter(online_status=online_type)
    else: 
        allnavi = navi.objects.all()
    print "the allnavi is %s" % allnavi;
    return render_to_response("skdomain/manage.html", locals(), RequestContext(request))




@login_required()
@permission_verify()
def edit(request,ids):
    obj = navi.objects.get(id=ids)
    
    temp_name = "skdomain/navi-header.html"
    if request.method == "POST":
        n_form = navi_form(request.POST,instance=obj)
        if n_form.is_valid():
            n_form.save()
            return HttpResponseRedirect(reverse('manage'))
    else:
        n_form = navi_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }
    
    return render_to_response('skdomain/edit.html', locals(), RequestContext(request))



