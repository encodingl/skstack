#! /usr/bin/env python
# -*- coding: utf-8 -*-
# update by guohongze@126.com
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from hashlib import sha1
from django.contrib import auth
from .forms import LoginUserForm, EditUserForm, ChangePasswordForm
from django.contrib.auth import get_user_model
from .forms import AddUserForm
from django.urls import reverse
from skaccounts.permission import permission_verify


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
 
    if request.method == 'GET' and 'next' in request.GET:
        next = request.GET['next']
    else:
        next = '/'
 
    if next == "/skaccounts/logout/":
        next = '/'
 
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST['next'])
    else:
        form = LoginUserForm(request)
 
    kwvars = {
        'request': request,
        'form':  form,
        'next': next,
    }
 
#     return render(request,'skaccounts/login.html', locals())
    return render(request,'skaccounts/login.html', locals())



@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
@permission_verify()
def user_list(request):
    temp_name = "skaccounts/accounts-header.html"
    all_user = get_user_model().objects.all()
    return render(request,'skaccounts/user_list.html', locals())


@login_required
@permission_verify()
def user_add(request):
    temp_name = "skaccounts/accounts-header.html"
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            form.save()
            return HttpResponseRedirect(reverse('user_list'))
    else:
        form = AddUserForm()

    kwvars = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
    }

    return render(request,'skaccounts/user_add.html', locals())


@login_required
@permission_verify()
def user_del(request):
    ids = request.GET.get('id', '')
    if ids:
        get_user_model().objects.filter(id=ids).delete()
        
    if request.method == 'POST':
        check_box_items = request.POST.getlist('check_box', [])
        if check_box_items:
            for n in check_box_items:
                print(n)
                get_user_model().objects.filter(id=n).delete()
    all_user = get_user_model().objects.all()
    return render(request,"skaccounts/user_list.html", locals())
    


@login_required
@permission_verify()
def user_edit(request, ids):
    user = get_user_model().objects.get(id=ids)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 3
    else:
        form = EditUserForm(instance=user)
    # ids = ids
    # kwvars = {
    #     'ids': ids,
    #     'form': form,
    #     'request': request,
    # }

    return render(request,'skaccounts/user_edit.html', locals())


@login_required
@permission_verify()
def reset_password(request, ids):
    user = get_user_model().objects.get(id=ids)
    newpassword = get_user_model().objects.make_random_password(length=10, allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
    print('====>ResetPassword:%s-->%s' % (user.username, newpassword))
    user.set_password(newpassword)
    user.save()

    kwvars = {
        'object': user,
        'newpassword': newpassword,
        'request': request,
    }

    return render(request,'skaccounts/reset_password.html', locals())


@login_required
def change_password(request):
    temp_name = "skaccounts/accounts-header.html"
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('logout'))
    else:
        form = ChangePasswordForm(user=request.user)

    kwvars = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
    }

    return render(request,'skaccounts/change_password.html', locals())