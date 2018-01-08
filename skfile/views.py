#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os,re,sys
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect,RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify,permission_verify_ids
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json
from models import Dirmanager
from forms import dirform
from collections import OrderedDict


#展示目录树结构

def dirlist(dir, fileList, tabnum=0):
    newDir = {"id": tabnum, "parent": tabnum - 1, "text": dir}
    if os.path.isfile(dir):
        # fileList.append(dir)
        fileList.append(newDir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            dirlist(newDir, fileList, tabnum + 1)
    fileList.append(newDir)
    return fileList


def index(request, *args, **kwargs):
    temp_name = "skfile/file-header.html"
    dirmanager = Dirmanager.objects.all()
    topdir=[]
    for dir in dirmanager:
        dirname=dir.dirname
        userfulpath=dirname.replace('\\','/')
        if userfulpath.endswith("/"):
            userfulpath=userfulpath[:-1]
            print userfulpath
        if not os.path.exists(userfulpath):
            print "路径错误"
        elif not os.path.exists(userfulpath):
            print "输入的不是目录"
        else:
            filelist = os.listdir(userfulpath)
            topdir.append(userfulpath)
            for dirpath in topdir:
              #list = dirlist(dirpath, OrderedDict())
              list = dirlist(dirpath, [])
              json_node = json.dumps(list, encoding="UTF-8", ensure_ascii=False)
              print json_node
   # print json_node
    #print topdir
    return render_to_response("skfile/file.html", locals(), RequestContext(request))


#管理配置目录 增删改查
def dir(request, *args, **kwargs):
    temp_name = "skfile/file-header.html"
    dirmanager = Dirmanager.objects.all()
    for dir in dirmanager:
        dirname=dir
        print dirname
    return render_to_response("skfile/dir.html", locals(), RequestContext(request))

def adddir(request, *args, **kwargs):
    if request.is_ajax() and request.method == 'POST':
        for key in request.POST:
            valuelist = request.POST.getlist(key)
            #print valuelist
            for i in valuelist:
                 print i
            order = Dirmanager.objects.create(dirname=i)
    return HttpResponse("pl")

def dir_delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    Dirmanager.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('file'))


def str2gb(args):
    return str(args).encode('gb2312')

def dir_edit(request,ids):
    dir_edit = Dirmanager.objects.get(id=ids)
    temp_name = "skyw/yw-header.html"
    if request.method=="POST":
        nform = dirform(request.POST,instance=dir_edit)
        if nform.is_valid():
            nform.save()
            tips = u"编辑成功！"
            display_control = ""
        else:
            tips = u"编辑失败！"
            display_control = ""
    else:
        display_control = "none"
        nform = dirform(instance=dir_edit)
    return render_to_response('skfile/dir_edit.html',locals(),RequestContext(request))


def file_history(request, *args, **kwargs):
    temp_name = "skfile/file-header.html"
    return render_to_response("skfile/history.html", locals(), RequestContext(request))

