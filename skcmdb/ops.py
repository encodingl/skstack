# coding:utf-8
#from Tkconstants import W

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from skaccounts.permission import permission_verify
from skcmdb.api import pages, get_object
from skcmdb.forms import IdcForm, EnvForm, YwGroupForm, MiddleTypeForm, AssetForm, AppForm, HostGroupForm, DbSourceForm, \
    UrlForm, WhileIpForm
from skcmdb.models import Env, YwGroup, MiddleType, ASSET_STATUS, App, HostGroup, DbSource, KafkaTopic, Url, MAP_TYPE, \
    WhileIp
from skaccounts.models import UserInfo
import commands


@login_required()
@permission_verify()
def opssa_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    opssa_info = UserInfo.objects.filter(type__gte=1).filter(type__lte=5)
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


@login_required
@permission_verify()
def env_edit(request, ids):
    status = 0
    obj = get_object(Env, id=ids)
    if request.method == 'POST':
        af = EnvForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = EnvForm(instance=obj)
    return render_to_response('skcmdb/env_edit.html', locals(), RequestContext(request))


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
        desc = request.POST.get('desc')
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
    status = request.GET.get('status', '')
    keyword = request.GET.get('keyword', '')

    app_find = App.objects.all()

    if sa_name:
        app_find = app_find.filter(sa__nickname__contains=sa_name)

    if env_name:
        app_find = app_find.filter(env__name__contains=env_name)

    if ywgroup_name:
        app_find = app_find.filter(ywgroup__name__contains=ywgroup_name)

    if status:
        app_find = app_find.filter(status__contains=status)

    if keyword:
        app_find = app_find.filter(
            Q(name__contains=keyword) |
            Q(ywgroup__name__contains=keyword) |
            Q(sa__nickname__contains=keyword) |
            Q(env__name__contains=keyword) |
            Q(status__contains=keyword) |
            Q(descrition__contains=keyword)
        )

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
    obj = get_object(App, id=ids)
    if request.method == 'POST':
        af = AppForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = AppForm(instance=obj)

    return render_to_response('skcmdb/app_edit.html', locals(), RequestContext(request))


@login_required
@permission_verify()
def url_list(request):
    temp_name = "skcmdb/cmdb-header.html"

    sa_info = UserInfo.objects.filter(type=1)
    env_info = Env.objects.all()
    ywgroup_info = YwGroup.objects.all()
    type_info = MAP_TYPE
    status_info = ASSET_STATUS

    sa = request.GET.get('sa', '')
    env = request.GET.get('env', '')
    ywgroup = request.GET.get('ywgroup', '')
    type = request.GET.get('type', '')
    status = request.GET.get('status', '')

    obj_info = Url.objects.all()

    if sa:
        obj_info = obj_info.filter(sa__nickname__contains=sa)
    if env:
        obj_info = obj_info.filter(env__name__contains=env)
    if ywgroup:
        obj_info = obj_info.filter(ywgroup__name__contains=ywgroup)
    if type:
        obj_info = obj_info.filter(type=type)
    if status:
        obj_info = obj_info.filter(status=status)
    return render_to_response('skcmdb/url_list.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def url_add(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == "POST":
        a_form = UrlForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        a_form = UrlForm()
    return render_to_response("skcmdb/url_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def url_del(request):
    url_id = request.GET.get('id', '')
    if url_id:
        Url.objects.filter(id=url_id).delete()

    if request.method == 'POST':
        url_id_all = str(request.POST.get('url_id_all', ''))
        if url_id_all:
            for url_id in url_id_all.split(','):
                url = get_object(Url, id=url_id)
                url.delete()
    return HttpResponse(u'删除成功')


@login_required
@permission_verify()
def url_edit(request, ids):
    status = 0
    obj = get_object(Url, id=ids)
    if request.method == 'POST':
        af = UrlForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = UrlForm(instance=obj)
    return render_to_response('skcmdb/url_edit.html', locals(), RequestContext(request))


@login_required
@permission_verify()
def kafka_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    kafka_info = KafkaTopic.objects.all()
    return render_to_response('skcmdb/kafka_list.html', locals(), RequestContext(request))


@login_required
@permission_verify()
def kafka_update(request):
    temp_name = "skcmdb/cmdb-header.html"
    cmd = "ssh 10.8.45.103 /opt/soft/kafka/bin/kafka-topics.sh --zookeeper 10.8.45.103:2181 --list"
    code, result = commands.getstatusoutput(cmd)
    if code == 0:
        data = result.split('\n')
        l = list(KafkaTopic.objects.values_list('name'))
        l_data = []
        for i in l:
            l_data.append(i[0])
        for d in data:
            if d not in l_data:
                KafkaTopic.objects.create(name=d)
        for d in l_data:
            if d not in data:
                KafkaTopic.objects.get(name=d).delete()
        return HttpResponse(u'更新成功 .')
    return HttpResponse(u'更新 Error!')


@login_required()
@permission_verify()
def dbsource_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    obj_info = DbSource.objects.all()
    return render_to_response('skcmdb/dbsource_list.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def dbsource_add(request):
    print "data=", request.method
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == "POST":
        obj_form = DbSourceForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = DbSourceForm()
    return render_to_response("skcmdb/dbsource_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def dbsource_del(request):
    id = request.GET.get('id', '')
    if id:
        DbSource.objects.filter(id=id).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def dbsource_edit(request, ids):
    obj = DbSource.objects.get(id=ids)
    pwd = obj.password
    status = 0
    if request.method == "POST":
        form = DbSourceForm(request.POST, instance=obj)
        if form.is_valid():
            if not obj.password:
                obj.password = pwd
            form.save()
            status = 1
            # else:
            #     status = 2
    else:
        form = DbSourceForm(instance=obj)
    return render_to_response("skcmdb/dbsource_edit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def whileip_list(request):
    temp_name = "skcmdb/cmdb-header.html"
    obj_info = WhileIp.objects.all()
    return render_to_response('skcmdb/whileip_list.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def whileip_add(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == "POST":
        obj_form = WhileIpForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = WhileIpForm()
    return render_to_response("skcmdb/whileip_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def whileip_del(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == 'POST':
        obj_items = request.POST.getlist('idc_check', [])
        print obj_items
        if obj_items:
            for n in obj_items:
                WhileIp.objects.filter(id=n).delete()
    return HttpResponseRedirect(reverse('whileip_list'), RequestContext(request))


@login_required
@permission_verify()
def whileip_edit(request, ids):
    status = 0
    obj = get_object(WhileIp, id=ids)
    if request.method == 'POST':
        af = WhileIpForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = WhileIpForm(instance=obj)
    return render_to_response('skcmdb/whileip_edit.html', locals(), RequestContext(request))

