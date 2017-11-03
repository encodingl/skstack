#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
import sys
from skyw.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect,RequestContext
from forms import devopsform,rotaform,noticeform
from django.core.urlresolvers import reverse
import json
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from collections import OrderedDict
# Create your views here.

def index(request):
    temp_name = "skyw/yw-header.html"
    person = Devops.objects.all()
    rota = Rota.objects.all()
    notice = Notice.objects.all()
    events = event.objects.all()
    platform=Platform.objects.all()

    # 先对人员j进行分类，拿到分类值班人员信息，再拿到轮班人员的信息。周取%，
    # 1.先区分应用运维和dba运维，根据区分的人员拿到对应的信息，应用运维组成lists。dba运维组成lists。放入运维值班表的固定td
    # 2.然后再获取轮班spell参数。组成list。放入运维值班表中的轮班td。
    # type = Rota.objects.select_related().all().values_list('name__type')
    yw_list=OrderedDict()
    dba_list=OrderedDict()
    yw_spell_list=OrderedDict()
    dba_spell_list=OrderedDict()
    telarrdba=OrderedDict()
    for i in rota:
            names = Rota.objects.get(name=i.name)
            types=names.name.type
            emergency_contact=i.emergency_contact
            print emergency_contact
            if types == 1 and i.emergency_contact == 1 and i.iphone_rota==0:
               yw_list[str(i.name.nickname)]=[str(i.iphone.iphone)]
               if i.spell==0:
                  yw_spell_list[str(i.name.nickname)] = [str(i.iphone.iphone)]
            elif types == 4 and i.emergency_contact == 1:
                dba_list[str(i.name.nickname)] = [str(i.iphone.iphone)]
                if i.spell==0:
                    dba_spell_list[str(i.name.nickname)]=[str(i.iphone.iphone)]
                if i.iphone_rota==0:
                    telarrdba[str(i.name.nickname)]=[str(i.iphone.iphone)]
            elif  i.emergency_contact == 0:
                print i.name
            else:
                print "error"
    dba_spell_list=json.dumps(dba_spell_list,encoding="UTF-8",ensure_ascii=False)
    yw_spell_list=json.dumps(yw_spell_list,encoding="UTF-8",ensure_ascii=False)
    print dba_spell_list
    telarr =dict(telarrdba.items()+yw_list.items())
    telarr=json.dumps(telarr,encoding="UTF-8",ensure_ascii=False)
    print telarr

    type = PlatFormclass.objects.all()
    d1={}
    list=[]
    for  name in type:
        #print name
       platformclass1 = PlatFormclass.objects.get(platform_class=name)
       admin_obj = platformclass1.platform_set.all()
       for admin_line in admin_obj:
          platformname = admin_line.platform_name
          platformurl= admin_line.platform_url
          d1.setdefault(str(name),[]).append([platformname,platformurl])
        #print d1
    dicts =json.dumps(d1,encoding="UTF-8",ensure_ascii=False)
    #print dicts
    #print d1

    return render_to_response("index.html", locals(), RequestContext(request))
@login_required()
@permission_verify()
def list(request):
    temp_name = "skyw/yw-header.html"
    person = Devops.objects.all()
    rota = Rota.objects.all()
    notice = Notice.objects.all()
    events = event.objects.all()
    platform =  Platform.objects.all()
    platformclasss=PlatFormclass.objects.all()
    for yw in person:
       name = yw.name
       iphone = yw.iphone
    return render_to_response("skyw/list.html", locals(), RequestContext(request))

def add(request):
    temp_name = "skyw/yw-header.html"
    if request.method == "POST":
       devops=devopsform(request.POST)
       if devops.is_valid(): 
           devops.save()
           tips = u'增加成功'
           display_control=""
       else:
           tips = u"增加失败"
           display_control = ""
    else:
        devops = devopsform()
        tips = u"空数据"
    return render_to_response("skyw/add.html", locals(), RequestContext(request))

def delete(request,ids):
    #yuming=get_object_or_404(yuming,pk=int(id))
    Devops.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('list'))
def str2gb(args):
    return str(args).encode('gb2312')

def edit(request,ids):
    devops_edit = Devops.objects.get(id=ids)
    temp_name = "skyw/yw-header.html"
    if request.method=="POST":
        nform = devopsform(request.POST,instance=devops_edit)
        if nform.is_valid():
            nform.save()
            tips = u"编辑成功！"
            display_control = ""
        else:
            tips = u"编辑失败！"
            display_control = ""
    else:
        nform= devopsform(instance=devops_edit)
    return render_to_response('skyw/edit.html',locals(),RequestContext(request))




