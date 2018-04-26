#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, RequestContext
from forms import Record_form
from forms import Track_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.core.urlresolvers import reverse
from models import Record
from models import Track


@login_required()
@permission_verify()
def track(request):
    temp_name = "skrecord/navi-header.html"
    track_info = Track.objects.all()
#    allnavi = navi.objects.all()
    return render_to_response("skrecord/track.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def add(request):
    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        track_form = Track_form(request.POST, request.FILES)

        if track_form.is_valid():
            Track.user = request.user
            title = track_form.cleaned_data['title']
            trackclass = track_form.cleaned_data['trackclass']
            trackdescribe = track_form.cleaned_data['trackdescribe']
            trackdispose = track_form.cleaned_data['trackdispose']
            #tracktime = track_form.cleaned_data['tracktime']
            status = track_form.cleaned_data['status']
            remarks = track_form.cleaned_data['remarks']
            user = Track.objects.create(user=Track.user, title=title, trackclass=trackclass, trackdescribe=trackdescribe, trackdispose=trackdispose, status=status, remarks=remarks)
            #track_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skrecord/track_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        track_form = Track_form()

        return render_to_response("skrecord/track_add.html", locals(), RequestContext(request))



@login_required
@permission_verify()
def track_delete(request, ids):
    Track.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('track'))

@login_required()
@permission_verify()
def message(request, EVENT_STATUS=None):
    temp_name = "skrecord/navi-header.html"

    event_status = EVENT_STATUS
    P_type = request.GET.get('P_type', '')
    print "p_type value:%s" % P_type
    if P_type:
        allnavi = Track.objects.filter(P_status=P_type)
    else:
        allnavi = Track.objects.all()
    print "the allnavi is %s" % allnavi;
    return render_to_response("skrecord/track.html", locals(), RequestContext(request))




@login_required()
@permission_verify()
def edit(request,ids):
    obj = Track.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        track_form = Track_form(request.POST,instance=obj)
        if track_form.is_valid():
            track_form.save()
            return HttpResponseRedirect(reverse('track'))
    else:
        track_form = Track_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render_to_response('skrecord/track_edit.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def detail(request,ids):
    obj = Track.objects.get(id=ids)

    temp_name = "skrecord/navi-header.html"
    if request.method == "POST":
        track_form = Track_form(request.POST,instance=obj)
        if track_form.is_valid():
            track_form.save()
            return HttpResponseRedirect(reverse('track'))
    else:
        track_form = Track_form(instance=obj)
#     print "the n_form is:%s" % n_form
#     kwvars = {
#         'temp_name': temp_name,
#         'ids': ids,
#         'n_form': n_form,
#         'request': request,
#     }

    return render_to_response('skrecord/track_detail.html', locals(), RequestContext(request))




