#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from .forms import Record_form
from .forms import Faq_form
from .forms import Assessment_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.core.urlresolvers import reverse
from .models import Record
from .models import Faq
from .models import Assessment


@login_required()
@permission_verify()
def assessment(request):
    temp_name = "skrecord/navi-header.html"
    assessment_info = Assessment.objects.all()
#    allnavi = navi.objects.all()
    return render_to_response("skrecord/assessment.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        assessment_form = Assessment_form(request.POST)

        if assessment_form.is_valid():
            assessment_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render_to_response("skrecord/assessment_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        assessment_form = Assessment_form()

        return render_to_response("skrecord/assessment_add.html", locals(), RequestContext(request))



@login_required
@permission_verify()
def assessment_delete(request, ids):
    Assessment.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('assessment'))

@login_required()
@permission_verify()
def message(request):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print("p_type value:%s" % P_type)
    if P_type:
        allnavi = Assessment.objects.filter(P_status=P_type)
    else:
        allnavi = Assessment.objects.all()
    print("the allnavi is %s" % allnavi);
    return render_to_response("skrecord/assessment.html", locals(), RequestContext(request))




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Assessment.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        assessment_form = Assessment_form(request.POST,instance=obj)
        if assessment_form.is_valid():
            assessment_form.save()
            return HttpResponseRedirect(reverse('assessment'))
    else:
        assessment_form = Assessment_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render_to_response('skrecord/assessment_edit.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def detail(request,ids):
    obj = Assessment.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        assessment_form = Assessment_form(request.POST,instance=obj)
        if assessment_form.is_valid():
            assessment_form.save()
            return HttpResponseRedirect(reverse('assessment'))
    else:
        assessment_form = Assessment_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render_to_response('skrecord/assessment_detail.html', locals(), RequestContext(request))




