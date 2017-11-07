#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, RequestContext
from forms import Record_form
from forms import Faq_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.core.urlresolvers import reverse
from models import Record
from models import Faq


@login_required()
@permission_verify()
def faq(request):
    temp_name = "skrecord/navi-header.html"
    faq_info = Faq.objects.all()
#    allnavi = navi.objects.all()
    return render_to_response("skrecord/faq.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        faq_form = Faq_form(request.POST)

        if faq_form.is_valid():
            faq_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skrecord/faq_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        faq_form = Faq_form()

        return render_to_response("skrecord/faq_add.html", locals(), RequestContext(request))



@login_required
@permission_verify()
def faq_delete(request, ids):
    Faq.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('faq'))

@login_required()
@permission_verify()
def message(request):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print "p_type value:%s" % P_type
    if P_type:
        allnavi = Faq.objects.filter(P_status=P_type)
    else:
        allnavi = Faq.objects.all()
    print "the allnavi is %s" % allnavi;
    return render_to_response("skrecord/faq.html", locals(), RequestContext(request))




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Faq.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        faq_form = Faq_form(request.POST,instance=obj)
        if faq_form.is_valid():
            faq_form.save()
            return HttpResponseRedirect(reverse('faq'))
    else:
        faq_form = Faq_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render_to_response('skrecord/faq_edit.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def detail(request,ids):
    obj = Faq.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        faq_form = Faq_form(request.POST,instance=obj)
        if faq_form.is_valid():
            faq_form.save()
            return HttpResponseRedirect(reverse('faq'))
    else:
        faq_form = Faq_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render_to_response('skrecord/faq_detail.html', locals(), RequestContext(request))



