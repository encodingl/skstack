#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect,RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json
from models import Dirmanager
from forms import dirform

@ensure_csrf_cookie
#展示目录树结构
def index(request):
    temp_name = "skfile/file-header.html"
    return render_to_response("skfile/index.html", locals(), RequestContext(request))

#管理配置目录 增删改查
def dir(request):
    temp_name = "skfile/file-header.html"
    dirmanager = Dirmanager.objects.all()
    for i in dirmanager:
        print i
    return render_to_response("skfile/dir.html", locals(), RequestContext(request))

def adddir(request):
    if request.is_ajax() and request.method == 'POST':
        for key in request.POST:
            valuelist = request.POST.getlist(key)
            #print valuelist
            for i in valuelist:
                 print i
            order = Dirmanager.objects.create(dirname=i)
    return HttpResponse("pl")

@login_required()
@permission_verify()
def dir_delete(request,ids):
    Dirmanager.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('dir'))
def str2gb(args):
    return str(args).encode('gb2312')


def history(request):
    temp_name = "skfile/file-header.html"
    return render_to_response("skfile/history.html", locals(), RequestContext(request))

