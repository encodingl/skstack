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
from skaccounts.permission import permission_verify
# Create your views here.



def platform_list(request):
    temp_name = "skyw/yw-header.html"
    type = PlatFormclass.objects.all()
    d1={}
    list=[]
    for  name in type:
        print name
        platformclass1 = PlatFormclass.objects.get(platform_class=name)
        admin_obj = platformclass1.platform_set.all()
        for admin_line in admin_obj:
          platformname = admin_line.platform_name
          platformurl= admin_line.platform_url
          #print platformname
          #print platformurl
          #context=platformname +"," + platformurl
          d1.setdefault(str(name),[]).append([platformname,platformurl])
        print d1
    dicts =json.dumps(d1,encoding="UTF-8",ensure_ascii=False)
    print dicts

    return render_to_response("skyw/platform.html",locals(), RequestContext(request))

def platformclass_add(request):
    temp_name = "skyw/yw-header.html"
    if request.method == "POST":
       platformclasss =  platformclassform(request.POST)
       if platformclasss.is_valid():

           platformclasss.save()
           tips = u'增加成功'
           return HttpResponseRedirect(reverse('platformclass_add'))
       else:
           tips = u"增加失败"
           displ_control = ""
    else:

        platformclasss = platformclassform()
        tips = u"空数据"
    return render_to_response("skyw/platformclass_add.html", locals(), RequestContext(request))

def platformclass_delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    PlatFormclass.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('list'))

def platformclass_edit(request,ids):
    platformclassedit = PlatFormclass.objects.get(id=ids)
    temp_name = "skyw/yw-header.html"
    if request.method=="POST":
        platformclassforms = platformclassform(request.POST,instance=platformclassedit)
        if platformclassforms.is_valid():
            platformclassforms.save()
            return HttpResponseRedirect(reverse('platform_list'))
    else:
        platformclassforms= platformclassform(instance=platformclassedit)
    return render_to_response('skyw/platformclass_edit.html',locals(),RequestContext(request))

def platform_add(request):
    temp_name = "skyw/yw-header.html"
    if request.method == "POST":

       platform = platformform(request.POST)
       if platform.is_valid() :
           platform.save()

           tips = u'增加成功'
           return HttpResponseRedirect(reverse('platform_add'))
       else:
           tips = u"增加失败"
           displ_control = ""
    else:
        platform = platformform()
        tips = u"空数据"
    return render_to_response("skyw/platform_add.html", locals(), RequestContext(request))

def platform_delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    Platform.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('list'))
def str2gb(args):
    return str(args).encode('gb2312')

def platform_edit(request,ids):
    platformedit = Platform.objects.get(id=ids)
    temp_name = "skyw/yw-header.html"
    if request.method=="POST":
        nform = platformform(request.POST,instance=platformedit)
        if nform.is_valid():
            nform.save()
            return HttpResponseRedirect(reverse('platform_list'))
    else:
        nform= platformform(instance=platformedit)
    return render_to_response('skyw/platform_edit.html',locals(),RequestContext(request))



