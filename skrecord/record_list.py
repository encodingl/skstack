#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, RequestContext
from .forms import Record_form
from .forms import Record_list_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.core.urlresolvers import reverse
from .models import Record
from .models import Record_list


@login_required()
@permission_verify()
def record_list(request):
    temp_name = "skrecord/navi-header.html"
    record_list_info = Record_list.objects.all()
#    allnavi = navi.objects.all()
    return render_to_response("skrecord/record_list.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        record_list_form = Record_list_form(request.POST)

        if record_list_form.is_valid():
            record_list_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skrecord/record_list_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        record_list_form = Record_list_form()

        return render_to_response("skrecord/record_list_add.html", locals(), RequestContext(request))



@login_required
@permission_verify()
def record_list_delete(request, ids):
    Record_list.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('record_list'))

@login_required()
@permission_verify()
def message(request):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print "p_type value:%s" % P_type
    if P_type:
        allnavi = Record_list.objects.filter(P_status=P_type)
    else:
        allnavi = Record_list.objects.all()
    print "the allnavi is %s" % allnavi;
    return render_to_response("skrecord/record_list.html", locals(), RequestContext(request))




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Record_list.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        record_list_form = Record_list_form(request.POST,instance=obj)
        if record_list_form.is_valid():
            record_list_form.save()
            return HttpResponseRedirect(reverse('record_list'))
    else:
        record_list_form = Record_list_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render_to_response('skrecord/record_list_edit.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def detail(request,ids):
    obj = Record_list.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        record_list_form = Record_list_form(request.POST,instance=obj)
        if record_list_form.is_valid():
            record_list_form.save()
            return HttpResponseRedirect(reverse('record_list'))
    else:
        record_list_form = Record_list_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render_to_response('skrecord/record_list_detail.html', locals(), RequestContext(request))




