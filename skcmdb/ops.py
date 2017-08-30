#coding:utf-8
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from skaccounts.permission import permission_verify
from skcmdb.api import pages, get_object
from skcmdb.forms import IdcForm,EnvForm, YwGroupForm, MiddleTypeForm, AssetForm, AppForm, HostGroupForm
from skcmdb.models import Env, YwGroup, MiddleType, ASSET_STATUS,App, ASSET_TYPE,HostGroup
from skaccounts.models import UserInfo


@login_required()
@permission_verify()
def opssa_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    opssa_info = UserInfo.objects.filter(type=1)
    return render_to_response('skcmdb/opssa_list.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def env_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    obj_info = Env.objects.all()
    return render_to_response('skcmdb/env_list.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def env_add(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == "POST":
        obj_form = EnvForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skcmdb/env_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        obj_form = EnvForm()
        return render_to_response("skcmdb/env_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def env_del(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == 'POST':
        obj_items = request.POST.getlist('idc_check', [])
        if obj_items:
            for n in obj_items:
                Env.objects.filter(id=n).delete()
    obj_info = Env.objects.all()
    return render_to_response("skcmdb/env_list.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def env_edit(request, ids):
    obj = Env.objects.get(id=ids)
    return render_to_response("skcmdb/env_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def env_save(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        descrition = request.POST.get('descrition')
        obj_item = Env.objects.get(id=id)
        obj_item.name = name
        obj_item.address = address
        obj_item.descrition = descrition
        obj_item.save()
        status = 1
    else:
        status = 2
    return render_to_response("skcmdb/env_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def ywgroup_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    obj_info = YwGroup.objects.all()
    return render_to_response('skcmdb/ywgroup_list.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def ywgroup_add(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == "POST":
        obj_form = YwGroupForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skcmdb/ywgroup_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        obj_form = YwGroupForm()
        return render_to_response("skcmdb/ywgroup_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def ywgroup_del(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == 'POST':
        obj_items = request.POST.getlist('idc_check', [])
        if obj_items:
            for n in obj_items:
                YwGroup.objects.filter(id=n).delete()
    obj_info = YwGroup.objects.all()
    return render_to_response("skcmdb/ywgroup_list.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def ywgroup_edit(request, ids):
    obj = YwGroup.objects.get(id=ids)
    allidc = YwGroup.objects.all()
    return render_to_response("skcmdb/ywgroup_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def ywgroup_save(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        sa = request.POST.get('address')
        descrition = request.POST.get('descrition')
        obj_item = YwGroup.objects.get(id=id)
        obj_item.name = name
        obj_item.address = sa
        obj_item.descrition = descrition
        obj_item.save()
        status = 1
    else:
        status = 2
    return render_to_response("skcmdb/ywgroup_edit.html", locals(), RequestContext(request))



@login_required()
@permission_verify()
def hostgroup_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    obj_info = HostGroup.objects.all()
    return render_to_response('skcmdb/hostgroup_list.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def hostgroup_add(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == "POST":
        obj_form = HostGroupForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skcmdb/hostgroup_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        obj_form = HostGroupForm()
        return render_to_response("skcmdb/hostgroup_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def hostgroup_del(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == 'POST':
        obj_items = request.POST.getlist('g_check', [])
        if obj_items:
            for n in obj_items:
                HostGroup.objects.filter(id=n).delete()
    obj_info = HostGroup.objects.all()
    return render_to_response("skcmdb/hostgroup_list.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def hostgroup_edit(request, ids):
    obj = HostGroup.objects.get(id=ids)
    return render_to_response("skcmdb/hostgroup_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def hostgroup_save(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('descrition')
        obj_item = HostGroup.objects.get(id=id)
        obj_item.name = name
        obj_item.desc = desc
        obj_item.save()
        status = 1
    else:
        status = 2
    return render_to_response("skcmdb/hostgroup_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def middletype_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    obj_info = MiddleType.objects.all()
    return render_to_response('skcmdb/middletype_list.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def middletype_add(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == "POST":
        obj_form = MiddleTypeForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skcmdb/middletype_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        obj_form = MiddleTypeForm()
        return render_to_response("skcmdb/middletype_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def middletype_del(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == 'POST':
        obj_items = request.POST.getlist('idc_check', [])
        if obj_items:
            for n in obj_items:
                MiddleType.objects.filter(id=n).delete()
    obj_info = MiddleType.objects.all()
    return render_to_response("skcmdb/middletype_list.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def middletype_edit(request, ids):
    obj = MiddleType.objects.get(id=ids)
    allidc = MiddleType.objects.all()
    return render_to_response("skcmdb/middletype_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def middletype_save(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        descrition = request.POST.get('descrition')
        obj_item = MiddleType.objects.get(id=id)
        obj_item.name = name
        obj_item.descrition = descrition
        obj_item.save()
        status = 1
    else:
        status = 2
    return render_to_response("skcmdb/middletype_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def app_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    sa_info = UserInfo.objects.filter(type=1)
    env_info = Env.objects.all()
    ywgroup_info = YwGroup.objects.all()
    hostgroup_info = HostGroup.objects.all()
    status_info = ASSET_STATUS

    sa_name = request.GET.get('sa', '')
    env_name = request.GET.get('env', '')
    ywgroup_name = request.GET.get('ywgroup', '')
    hostgroup_name = request.GET.get('hostgroup', '')
    status = request.GET.get('status', '')
    keyword = request.GET.get('keyword', '')

    app_find = App.objects.all()


    if sa_name:
        app_find = app_find.filter(sa__nickname__contains=sa_name)

    if env_name:
        app_find = app_find.filter(env__name__contains=env_name)

    if ywgroup_name:
        app_find = app_find.filter(ywgroup__name__contains=ywgroup_name)

    if hostgroup_name:
        app_find = app_find.filter(hosttype__name__contains=hostgroup_name)

    if status:
        app_find = app_find.filter(status__contains=status)

    if keyword:
        app_find = app_find.filter(
            Q(hostname__contains=keyword) |
            Q(ip__contains=keyword) |
            Q(other_ip__contains=keyword) |
            Q(os__contains=keyword) |
            Q(vendor__contains=keyword) |
            Q(cpu_model__contains=keyword) |
            Q(cpu_num__contains=keyword) |
            Q(memory__contains=keyword) |
            Q(disk__contains=keyword) |
            Q(sn__contains=keyword) |
            Q(position__contains=keyword) |
            Q(memo__contains=keyword))

    app_list, p, apps, page_range, current_page, show_first, show_end = pages(app_find, request)
    return render_to_response('skcmdb/app_list.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def app_add(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == "POST":
        a_form = AppForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skcmdb/app_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        a_form = AppForm()
        return render_to_response("skcmdb/app_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def app_del(request):
    app_id = request.GET.get('id', '')
    if app_id:
        App.objects.filter(id=app_id).delete()

    if request.method == 'POST':
        app_batch = request.GET.get('arg', '')
        app_id_all = str(request.POST.get('app_id_all', ''))

        if app_batch:
            for app_id in app_id_all.split(','):
                app = get_object(App, id=app_id)
                app.delete()

    return HttpResponse(u'删除成功')


@login_required
@permission_verify()
def app_edit(request, ids):
    status = 0
    app_types = ASSET_TYPE
    obj = get_object(App, id=ids)
    if request.method == 'POST':
        af = AppForm(request.POST, instance=obj)
        if af.is_valid():
            print af.cleaned_data['belong_ip']

            af.save()
            status = 1
        else:
            status = 2
    else:
        af = AppForm(instance=obj)

    return render_to_response('skcmdb/app_edit.html', locals(), RequestContext(request))
