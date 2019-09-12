#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .forms import RoleListForm,RoleJobForm
from .models import RoleList,RoleJob
from skaccounts.permission import permission_verify


@login_required()
@permission_verify()
def role_add(request):
    temp_name = "skaccounts/accounts-header.html"
    if request.method == "POST":
        form = RoleListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
    else:
        form = RoleListForm()

    kwvars = {
        'temp_name': temp_name,
        'form': form,
        'request': request,
    }

    return render(request,'skaccounts/role_add.html',locals(),RequestContext(request))


@login_required()
@permission_verify()
def role_list(request):
    temp_name = "skaccounts/accounts-header.html"
    all_role = RoleList.objects.all()
    return render(request,'skaccounts/role_list.html', locals(),RequestContext(request))


@login_required()
@permission_verify()
def role_edit(request, ids):
    iRole = RoleList.objects.get(id=ids)
#     print "the iRole is:%s" % iRole
    temp_name = "skaccounts/accounts-header.html"
    if request.method == "POST":
        form = RoleListForm(request.POST,instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
    else:
        form = RoleListForm(instance=iRole)
#         print "the form is:%s" % form
    kwvars = {
        'temp_name': temp_name,
        'ids': ids,
        'form': form,
        'request': request,
    }

    return render(request,'skaccounts/role_edit.html', locals())


@login_required()
@permission_verify()
def role_del(request, ids):
    RoleList.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('role_list'))



@login_required
@permission_verify()
def role_job_add(request):
    temp_name = "skaccounts/accounts-header.html"
    if request.method == "POST":
        form = RoleJobForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_job_list'))
    else:
        form = RoleJobForm()

    kwvars = {
        'temp_name': temp_name,
        'form': form,
        'request': request,
    }

    return render(request,'skaccounts/role_job_add.html',locals(),RequestContext(request))


@login_required
@permission_verify()
def role_job_list(request):
    temp_name = "skaccounts/accounts-header.html"
    all_role = RoleJob.objects.all()
    return render(request,'skaccounts/role_job_list.html', locals(),RequestContext(request))


@login_required
@permission_verify()
def role_job_edit(request, ids):
    iRole = RoleJob.objects.get(id=ids)
#     print "the iRole is:%s" % iRole
    temp_name = "skaccounts/accounts-header.html"
    if request.method == "POST":
        form = RoleJobForm(request.POST,instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_job_list'))
    else:
        form = RoleJobForm(instance=iRole)
#         print "the form is:%s" % form
    kwvars = {
        'temp_name': temp_name,
        'ids': ids,
        'form': form,
        'request': request,
    }

    return render(request,'skaccounts/role_job_edit.html', locals())


@login_required
@permission_verify()
def role_job_del(request, ids):
    RoleJob.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('role_job_list'))


