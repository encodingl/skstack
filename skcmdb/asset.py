#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .forms import AssetForm
from lib.utils import mysql_execute
from lib.type import ASSET_TYPE
from .models import Host, Idc, HostGroup, ASSET_STATUS, Env, YwGroup, MiddleType, DbSource
from django.shortcuts import render_to_response, redirect, RequestContext, HttpResponse
from django.db.models import Q
from skcmdb.api import get_object
from skcmdb.api import pages, str2gb
import csv, datetime
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from skaccounts.models import UserInfo
from django.views.decorators.csrf import csrf_exempt
import sys
import importlib

importlib.reload(sys)


@login_required()
@permission_verify()
def other(request):
    return HttpResponse("敬请期待...")

@login_required()
@permission_verify()
def asset(request):
    temp_name = "skcmdb/cmdb-header.html"
    idc_info = Idc.objects.all()
    sa_info = UserInfo.objects.filter(type=1)
    env_info = Env.objects.all()
    ywgroup_info = YwGroup.objects.all()
    hosttype_info = HostGroup.objects.all()
    middletype_info = MiddleType.objects.all()

    host_list = Host.objects.all()
    group_info = HostGroup.objects.all()
    asset_status = ASSET_STATUS
    idc_name = request.GET.get('idc', '')
    sa_name = request.GET.get('sa', '')
    env_name = request.GET.get('env', '')
    ywgroup_name = request.GET.get('ywgroup', '')
    hostgroup_name = request.GET.get('hostgroup', '')
    middletype_name = request.GET.get('middletype', '')
    status = request.GET.get('status', '')
    keyword = request.GET.get('keyword', '')
    export = request.GET.get("export", '')
    group_id = request.GET.get("group_id", '')
    idc_id = request.GET.get("idc_id", '')
    asset_id_all = request.GET.getlist("id", '')

    if group_id:
        group = get_object(HostGroup, id=group_id)
        if group:
            asset_find = Host.objects.filter(group=group)
    elif idc_id:
        idc = get_object(Idc, id=idc_id)
        if idc:
            asset_find = Host.objects.filter(idc=idc)
    else:
        asset_find = Host.objects.all()

    if idc_name:
        asset_find = asset_find.filter(idc__name__contains=idc_name)

    if sa_name:
        asset_find = asset_find.filter(sa__nickname__contains=sa_name)

    if env_name:
        asset_find = asset_find.filter(env__name__contains=env_name)

    if ywgroup_name:
        asset_find = asset_find.filter(ywgroup__name__contains=ywgroup_name)

    if hostgroup_name:
        asset_find = asset_find.filter(group__name__contains=hostgroup_name)

    if middletype_name:
        asset_find = asset_find.filter(middletype__name__contains=middletype_name)

    if status:
        asset_find = asset_find.filter(status__contains=status)

    if keyword:
        asset_find = asset_find.filter(
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
    if export == "true":
        if asset_id_all:
            asset_find = []
            for asset_id in asset_id_all:
                asset = get_object(Host, id=asset_id)
                if asset:
                    asset_find.append(asset)
            response = HttpResponse(content_type='text/csv')
            now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
            file_name = 'hostsesset_cmdb_' + now + '.csv'
            response['Content-Disposition'] = "attachment; filename=" + file_name
            writer = csv.writer(response)
            writer.writerow([str2gb('主机名'), str2gb('IP地址'), str2gb('其它IP'), str2gb('主机分组'), str2gb('负责人'),
                             str2gb('运行环境'), str2gb('业务分组'), str2gb('主机类型'), str2gb('资产编号'), str2gb('设备状态'),
                             str2gb('操作系统'), str2gb('设备厂商'), str2gb('CPU型号'), str2gb('CPU核数'), str2gb('内存大小'),
                             str2gb('硬盘信息'), str2gb('SN号码'), str2gb('所在机房'), str2gb('所在位置'), str2gb('备注信息')])
            for h in asset_find:
                if h.status:
                    at_as = int(h.status)
                    a_status = ASSET_STATUS[at_as - 1][1]
                else:
                    a_status = ""
                if h.sa:
                    a_sa = h.sa.nickname
                else:
                    a_sa = ""
                writer.writerow([str2gb(h.hostname), h.ip, h.other_ip, str2gb(h.group), str2gb(a_sa), str2gb(h.env),
                                 str2gb(h.ywgroup), str2gb(h.middletype), str2gb(h.asset_no), str2gb(a_status),
                                 str2gb(h.os), str2gb(h.vendor), str2gb(h.cpu_model), str2gb(h.cpu_num),
                                 str2gb(h.memory), str2gb(h.disk), str2gb(h.sn), str2gb(h.idc), str2gb(h.position),
                                 str2gb(h.memo)])
            return response
    if export == "all":
        host = Host.objects.all()
        response = HttpResponse(content_type='text/csv')
        now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        file_name = 'hostsesset_cmdb_' + now + '.csv'
        response['Content-Disposition'] = "attachment; filename=" + file_name
        writer = csv.writer(response)
        writer.writerow([str2gb('主机名'), str2gb('IP地址'), str2gb('其它IP'), str2gb('主机分组'), str2gb('负责人'),
                         str2gb('运行环境'), str2gb('业务分组'), str2gb('主机类型'), str2gb('资产编号'), str2gb('设备状态'),
                         str2gb('操作系统'), str2gb('设备厂商'), str2gb('CPU型号'), str2gb('CPU核数'), str2gb('内存大小'),
                         str2gb('硬盘信息'), str2gb('SN号码'), str2gb('所在机房'), str2gb('所在位置'), str2gb('备注信息')])
        for h in host:
            if h.status:
                at_as = int(h.status)
                a_status = ASSET_STATUS[at_as - 1][1]
            else:
                a_status = ""
            if h.sa:
                a_sa = h.sa.nickname
            else:
                a_sa = ""
            writer.writerow(
                [str2gb(h.hostname), h.ip, h.other_ip, str2gb(h.group), str2gb(a_sa), str2gb(h.env), str2gb(h.ywgroup),
                 str2gb(h.middletype), str2gb(h.asset_no), str2gb(a_status), str2gb(h.os), str2gb(h.vendor),
                 str2gb(h.cpu_model), str2gb(h.cpu_num), str2gb(h.memory), str2gb(h.disk), str2gb(h.sn), str2gb(h.idc),
                 str2gb(h.position), str2gb(h.memo)])
        return response

    assets_list, p, assets, page_range, current_page, show_first, show_end = pages(asset_find, request)
    return render_to_response('skcmdb/index.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def asset_add(request):
    temp_name = "skcmdb/cmdb-header.html"
    if request.method == "POST":
        a_form = AssetForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = "增加成功！"
            display_control = ""
        else:
            tips = "增加失败！"
            display_control = ""
        return render_to_response("skcmdb/asset_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        a_form = AssetForm()
        return render_to_response("skcmdb/asset_add.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def asset_del(request):
    asset_id = request.GET.get('id', '')
    if asset_id:
        Host.objects.filter(id=asset_id).delete()

    if request.method == 'POST':
        asset_batch = request.GET.get('arg', '')
        asset_id_all = str(request.POST.get('asset_id_all', ''))

        if asset_batch:
            for asset_id in asset_id_all.split(','):
                asset = get_object(Host, id=asset_id)
                asset.delete()

    return HttpResponse('删除成功')


@login_required
@permission_verify()
def asset_edit(request, ids):
    status = 0
    obj = get_object(Host, id=ids)
    if request.method == 'POST':
        af = AssetForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = AssetForm(instance=obj)
    return render_to_response('skcmdb/asset_edit.html', locals(), RequestContext(request))


@login_required
@permission_verify()
def asset_import(request):
    local_idc_info = Idc.objects.all()
    local_group_info = HostGroup.objects.all()
    local_type_info = MiddleType.objects.all()

    dbsource_info = DbSource.objects.all()
    dbsource = request.GET.get('dbsource', '')

    if request.method == 'GET' and dbsource:
        source_idc_info = mysql_execute(dbsource, "select name from jasset_idc")
        source_group_info = mysql_execute(dbsource, "select name from jasset_assetgroup")
        source_type_info = ASSET_TYPE

    if request.method == 'POST':
        idc = request.GET.get('idc', '')
        hosttype = request.GET.get('hosttype', '')
        hostgroup = request.GET.get('hostgroup', '')
        l_idc = request.GET.get('l_idc', '')
        l_type = request.GET.get('l_type', '')
        l_hostgroup = request.GET.get('l_hostgroup', '')

        if dbsource and idc and hosttype and hostgroup and l_idc and l_type and l_hostgroup:
            source_idc_info = mysql_execute(dbsource, "select name from jasset_idc")
            source_group_info = mysql_execute(dbsource, "select name from jasset_assetgroup")
            source_type_info = ASSET_TYPE

            sql = '''select a.hostname,a.ip,a.system_type,a.cpu,a.memory,a.disk from jasset_asset as a,jasset_idc as b,jasset_AssetGroup as c,jasset_asset_group as d where c.name="%s" and c.id=d.assetgroup_id and a.id=d.asset_id and a.idc_id=b.id and b.name="%s" and a.asset_type="%s";''' % (
            hosttype, idc, int(hostgroup) if hostgroup else '')
            asset_list = mysql_execute(dbsource, sql)
            ip_list = []
            data = {}
            for asset in asset_list:
                data[asset[1]] = asset
                ip_list.append(asset[1])
            ips_list = list(Host.objects.values_list('ip'))
            local_ip_list = []
            for ips in ips_list:
                local_ip_list.append(ips[0])
            idc = Idc.objects.get(name=l_idc)
            hostgroup = HostGroup.objects.get(name=l_hostgroup)
            middletype = MiddleType.objects.get(name=l_type)
            for ip in ip_list:
                if ip not in local_ip_list:
                    Host.objects.create(hostname=data[ip][0],ip=data[ip][1],os=data[ip][2],cpu_model=data[ip][3],memory=data[ip][4],disk=data[ip][5],idc=idc,group=hostgroup,middletype=middletype)
                else:
                    host=Host.objects.get(ip=ip)
                    host.hostname=data[ip][0]
                    host.os=data[ip][2]
                    host.cpu_model=data[ip][3]
                    host.memory=data[ip][4]
                    host.disk=data[ip][5]
                    host.idc=idc
                    host.group=hostgroup
                    host.middletype=middletype
                    host.save()
            return HttpResponse('恭喜你,主机信息导入成功过 .')
        else:
            return HttpResponse('类型选择错误!!!')
    return render_to_response('skcmdb/asset_import.html', locals(), RequestContext(request))
