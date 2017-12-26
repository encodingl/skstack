#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from forms import PermissionListForm
from models import UserInfo, RoleList, PermissionList


def permission_verify():
    """
        权限认证模块,
        此模块会先判断用户是否是管理员（is_superuser为True），如果是管理员，则具有所有权限,
        如果不是管理员则获取request.user和request.path两个参数，判断两个参数是否匹配，匹配则有权限，反之则没有。
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            iUser = UserInfo.objects.get(username=request.user)
            # 判断用户如果是超级管理员则具有所有权限
            if not iUser.is_superuser:
                if not iUser.role:  # 如果用户无角色，直接返回无权限
                    return HttpResponseRedirect(reverse('permission_deny'))

                role_permission = RoleList.objects.get(name=iUser.role)
                role_permission_list = role_permission.permission.all()

                matchUrl = []
                for x in role_permission_list:
                    # 精确匹配，判断request.path是否与permission表中的某一条相符
                    if request.path == x.url or request.path.rstrip('/') == x.url:
                        matchUrl.append(x.url)
                    # 判断request.path是否以permission表中的某一条url开头
                    elif request.path.startswith(x.url):
                        matchUrl.append(x.url)
                    else:
                        pass

                print '%s---->matchUrl:%s' %(request.user,str(matchUrl))
                
                if len(matchUrl) == 0:
                    return HttpResponseRedirect(reverse('permission_deny'))
                
                args=[]
                for l in role_permission_list:
                    args.append(str(l.url))
#                 args=json.dumps(args)
                print args
            else:
                args=['/all/']

            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator

def permission_verify_ids():
    """
        权限认证模块,
        此模块会先判断用户是否是管理员（is_superuser为True），如果是管理员，则具有所有权限,
        如果不是管理员则获取request.user和request.path两个参数，判断两个参数是否匹配，匹配则有权限，反之则没有。
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            iUser = UserInfo.objects.get(username=request.user)
            # 判断用户如果是超级管理员则具有所有权限
            if not iUser.is_superuser:
                if not iUser.role:  # 如果用户无角色，直接返回无权限
                    return HttpResponseRedirect(reverse('permission_deny'))

                role_permission = RoleList.objects.get(name=iUser.role)
                role_permission_list = role_permission.permission.all()

                matchUrl = []
                for x in role_permission_list:
                    # 精确匹配，判断request.path是否与permission表中的某一条相符
                    if request.path == x.url or request.path.rstrip('/') == x.url:
                        matchUrl.append(x.url)
                    # 判断request.path是否以permission表中的某一条url开头
                    elif request.path.startswith(x.url):
                        matchUrl.append(x.url)
                    else:
                        pass

                print '%s---->matchUrl:%s' %(request.user,str(matchUrl))
                
                if len(matchUrl) == 0:
                    return HttpResponseRedirect(reverse('permission_deny'))
                # 非授权url前端栏目过滤
                
            else:
                pass
            
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator
@login_required
def permission_deny(request, *args, **kwargs):
    temp_name = "main-header.html"
    kwvars = {
        'temp_name': temp_name,
        'request': request,
    }

    return render_to_response('skaccounts/permission_deny.html', locals(), RequestContext(request))


@login_required
@permission_verify()
def permission_add(request, *args, **kwargs):
    temp_name = "skaccounts/accounts-header.html"
    if request.method == "POST":
        form = PermissionListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permission_list'))
    else:
        form = PermissionListForm()

    kwvars = {
        'temp_name': temp_name,
        'form': form,
        'request': request,
    }

    return render_to_response('skaccounts/permission_add.html', locals(), RequestContext(request))


@login_required
@permission_verify()
def permission_list(request, *args, **kwargs):
    all_permission = PermissionList.objects.all()
    temp_name = "skaccounts/accounts-header.html"
    return render_to_response('skaccounts/permission_list.html', locals())


@login_required
@permission_verify_ids()
def permission_edit(request, ids):
    temp_name = "skaccounts/accounts-header.html"
    iPermission = PermissionList.objects.get(id=ids)

    if request.method == "POST":
        form = PermissionListForm(request.POST, instance=iPermission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permission_list'))
    else:
        form = PermissionListForm(instance=iPermission)

    kwvars = {
        'temp_name': temp_name,
        'ids': ids,
        'form': form,
        'request': request,
    }

    return render_to_response('skaccounts/permission_edit.html', locals(), RequestContext(request))


@login_required
@permission_verify_ids()
def permission_del(request, ids):
    PermissionList.objects.filter(id=ids).delete()

    return HttpResponseRedirect(reverse('permission_list'))
