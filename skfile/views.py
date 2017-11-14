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
def tree(dirpath,level=1):
        os.path.split('%s' % (dirpath))[1]
        filelist = os.listdir('%s' % (dir))
        for num in range(len(filelist)):
            filename = filelist[num]
            path = dirpath + "/" + filename
            print path
            if os.path.isdir(dirpath + "/" + filename):
                #print filename, levedir + 1
                tree(dirpath,level+1)
                print tree
            else:
                print filename, level

def index(request):
    temp_name = "skfile/file-header.html"
    dirmanager = Dirmanager.objects.all()
    for dir in dirmanager:
        dirname=dir.dirname
        print dirname
        level=1
        tree('%s',level+1 %(dirname))


    return render_to_response("skfile/index.html", locals(), RequestContext(request))

#管理配置目录 增删改查
def dir(request):
    temp_name = "skfile/file-header.html"
    dirmanager = Dirmanager.objects.all()
    for dir in dirmanager:
        dirname=dir
        print dirname
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


def str2gb(args):
    return str(args).encode('gb2312')


def file_history(request):
    temp_name = "skfile/file-header.html"
    return render_to_response("skfile/history.html", locals(), RequestContext(request))

