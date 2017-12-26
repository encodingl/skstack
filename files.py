#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect,RequestContext
from django.core.urlresolvers import reverse
import json
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify,permission_verify_ids
def files(request, *args, **kwargs):
     temp_name = "skfile/file-header.html"
     path = ["/etc/ansible/project","/data/deploy/config"]

     dirList=[] #所有目录
     fileList=[] #所有目录下返回的文件列表
     for dir in path:
        print dir
        files = os.listdir(dir)
        for f in files:
          if(os.path.isdir(f)):
                    if(f[0]=='.'):
                       pass
                    else:
                        dirList.append(f)
          if(os.path.isfile(f)):
           fileList.append(f)
     print dirList,fileList  
     return render_to_response("skfile/index.html", locals(), RequestContext(request))
