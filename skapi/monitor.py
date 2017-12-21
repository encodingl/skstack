# coding:utf8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
import json

from skaccounts.permission import permission_verify

from models import AlarmUser, AlarmGroup, AlarmList, TokenAuth, UserPolicy, AlarmRecord, ZabbixRecord
from skapi.api import SendWeixin, SendMail, SendSms, SendMobile, SendDingding
from skapi.forms import AlarmUserForm, AlarmGroupForm, AlarmListForm, AddAlarmUserForm, TokenAuthForm, UserPolicyForm, \
    AlarmRecordForm, ZabbixRecordForm
from lib.com import get_object, config, cfg, configfile
from utils import initAlarmList
import logging

log = logging.getLogger('zabbix')


@login_required()
@permission_verify()
def index(request):
    temp_name = "skapi/api-header.html"
    alarmgroup_info = AlarmGroup.objects.all()
    alarmgroup_id = request.GET.get('alarmgroup', '')

    if alarmgroup_id:
        ag = AlarmGroup.objects.get(id=alarmgroup_id)
        obj_info = ag.alarmlist_set.all()
    else:
        temp = AlarmGroup.objects.first()
        if temp:
            obj_info = AlarmList.objects.filter(group=temp)
    return render_to_response('skapi/index.html', locals(), RequestContext(request))


def alarmlistedit(request, ids):
    obj = AlarmList.objects.get(id=ids)
    status = 0
    if request.method == "POST":
        form = AlarmListForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            status = 1
            # else:
            #     status = 2
    else:
        form = AlarmListForm(instance=obj)
    return render_to_response("skapi/alarmlistedit.html", locals(), RequestContext(request))


@login_required()
@permission_verify()
def userlist(request):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmUser.objects.all()
    return render_to_response('skapi/userlist.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def useradd(request):
    temp_name = "skapi/api-header.html"
    if request.method == "POST":
        obj_form = AddAlarmUserForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = AddAlarmUserForm()
    return render_to_response('skapi/useradd.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def userdel(request):
    id = request.GET.get('id', '')
    if id:
        auser = AlarmUser.objects.get(id=id)
        a_name = auser.name
        auser.delete()
        AlarmList.objects.filter(name=a_name).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def useredit(request, ids):
    temp_name = "skapi/api-header.html"
    status = 0
    obj = get_object(AlarmUser, id=ids)
    if request.method == 'POST':
        af = AlarmUserForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = AlarmUserForm(instance=obj)
    return render_to_response('skapi/useredit.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def policy(request):
    temp_name = "skapi/api-header.html"
    obj_info = UserPolicy.objects.all()
    return render_to_response('skapi/policy.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def policyadd(request):
    temp_name = "skapi/api-header.html"
    if request.method == "POST":
        obj_form = UserPolicyForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = UserPolicyForm()
    return render_to_response('skapi/policyadd.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def policydel(request):
    id = request.GET.get('id', '')
    if id:
        UserPolicy.objects.get(id=id).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def policyedit(request, ids):
    temp_name = "skapi/api-header.html"
    status = 0
    obj = get_object(UserPolicy, id=ids)
    if request.method == 'POST':
        af = UserPolicyForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = UserPolicyForm(instance=obj)
    return render_to_response('skapi/policyedit.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def grouplist(request):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmGroup.objects.all()
    return render_to_response('skapi/grouplist.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def groupadd(request):
    temp_name = "skapi/api-header.html"
    if request.method == "POST":
        obj_form = AlarmGroupForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            group = AlarmGroup.objects.get(name=obj_form.cleaned_data['name'])
            initAlarmList(group)
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = AlarmGroupForm()
    return render_to_response('skapi/groupadd.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def groupdel(request):
    id = request.GET.get('id', '')
    if id:
        ag = AlarmGroup.objects.get(id=id)
        AlarmList.objects.filter(group=ag).delete()
        ag.delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def groupedit(request, ids):
    temp_name = "skapi/api-header.html"
    status = 0
    obj = get_object(AlarmGroup, id=ids)
    if request.method == 'POST':
        af = AlarmGroupForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            group = AlarmGroup.objects.get(id=ids)
            initAlarmList(group)
            status = 1
        else:
            status = 2
    else:
        af = AlarmGroupForm(instance=obj)
    return render_to_response('skapi/groupedit.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def setuplist(request):
    temp_name = "skapi/api-header.html"
    cfg = config()
    if request.method == 'POST':
        email_host = request.POST.get('email_host', '')
        email_port = request.POST.get('email_port', '')
        email_user = request.POST.get('email_user', '')
        email_password = request.POST.get('email_password', '')
        weixin_status = request.POST.get('weixin_status', '')
        email_status = request.POST.get('email_status', '')
        sms_status = request.POST.get('sms_status', '')
        dd_status = request.POST.get('dd_status', '')
        tel_status = request.POST.get('tel_status', '')
        weixin_gurl = request.POST.get('weixin_gurl', '')
        weixin_purl = request.POST.get('weixin_purl', '')
        weixin_cropid = request.POST.get('weixin_cropid', '')
        weixin_secret = request.POST.get('weixin_secret', '')
        sms_api = request.POST.get('sms_api', '')
        linkedsee_api = request.POST.get('linkedsee_api', '')
        szyw_token = request.POST.get('szyw_token', '')
        zhoujie_token = request.POST.get('zhoujie_token', '')
        zabbix_status = request.POST.get('zabbix_status', '')
        cfg.set('email', 'email_host', email_host)
        cfg.set('email', 'email_port', email_port)
        cfg.set('email', 'email_user', email_user)
        cfg.set('email', 'email_password', email_password)
        cfg.set('api', 'weixin_status', weixin_status)
        cfg.set('api', 'email_status', email_status)
        cfg.set('api', 'sms_status', sms_status)
        cfg.set('api', 'dd_status', dd_status)
        cfg.set('api', 'tel_status', tel_status)
        cfg.set('api', 'weixin_gurl', weixin_gurl)
        cfg.set('api', 'weixin_purl', weixin_purl)
        cfg.set('api', 'weixin_cropid', weixin_cropid)
        cfg.set('api', 'weixin_secret', weixin_secret)
        cfg.set('api', 'sms_api', sms_api)
        cfg.set('api', 'linkedsee_api', linkedsee_api)
        cfg.set('api', 'szyw_token', szyw_token)
        cfg.set('api', 'zhoujie_token', zhoujie_token)
        cfg.set('record', 'zabbix_status', zabbix_status)
        fp = open(configfile, 'w')
        cfg.write(fp)
        fp.close()
        tips = u"保存成功！"
        display_control = ""
    else:
        display_control = "none"
        email_host = cfg.get('email', 'email_host')
        email_port = cfg.get('email', 'email_port')
        email_user = cfg.get('email', 'email_user')
        email_password = cfg.get('email', 'email_password')
        weixin_status = cfg.get('api', 'weixin_status')
        email_status = cfg.get('api', 'email_status')
        sms_status = cfg.get('api', 'sms_status')
        dd_status = cfg.get('api', 'dd_status')
        tel_status = cfg.get('api', 'tel_status')
        weixin_gurl = cfg.get('api', 'weixin_gurl')
        weixin_purl = cfg.get('api', 'weixin_purl')
        weixin_cropid = cfg.get('api', 'weixin_cropid')
        weixin_secret = cfg.get('api', 'weixin_secret')
        sms_api = cfg.get('api', 'sms_api')
        linkedsee_api = cfg.get('api', 'linkedsee_api')
        szyw_token = cfg.get('api', 'szyw_token')
        zhoujie_token = cfg.get('api', 'zhoujie_token')
        zabbix_status = cfg.get('record', 'zabbix_status')

    return render_to_response('skapi/setup.html', locals(), RequestContext(request))


def zabbixalart(request):
    token = request.GET.get('token', '')
    if request.method == 'POST' and token == cfg.get('token', 'token'):
        zabbix_subject = request.POST.get('subject', '')
        zabbix_content = request.POST.get('content', '')
        content = zabbix_content.split("||")
        type = request.POST.get('type', '')
        log.info('[token:' + token + ']' + '[subject:' + zabbix_subject + ']' + '[content:' + zabbix_content + ']')
        sub_data = zabbix_subject.split(',', 1)
        groupid = int(sub_data[0])
        subject = sub_data[1]
        ag_obj = AlarmGroup.objects.get(id=groupid)
        serial = ag_obj.serial
        message = u"[故障名称]:%s\n[故障主机]:%s\n[故障时间]:%s\n[事件ID]:%s\n[错误日志]:%s\n" % (
        content[0], content[2], content[3], content[4], content[5])
        if type == 'appname':
            sub_data = zabbix_subject.split(',', 2)
            appname = sub_data[1]
            if config().get('record', 'zabbix_status') == 'On':
                zr = ZabbixRecord.objects.create(name='zabbix', token=token, subject=subject, appname=appname,
                                                 status=content[1], host=content[2],
                                                 event=content[4], content=content[5])
            userlist = AlarmList.objects.filter(group=ag_obj, weixin_status=1).filter(
                Q(name__app__name=appname) | Q(name__app__name='all')).distinct()
            wxlist = [wx.name.email for wx in userlist]
            SendWeixin().send('|'.join(wxlist), message, serial)
            userlist = AlarmList.objects.filter(group=ag_obj, email_status=1).filter(
                Q(name__app__name=appname) | Q(name__app__name='all')).distinct()
            emaillist = [ul.name.email for ul in userlist]
            SendMail().send(subject, emaillist, message)
            userlist = AlarmList.objects.filter(group=ag_obj, sms_status=1).filter(
                Q(name__app__name=appname) | Q(name__app__name='all')).distinct()
            tellist = [ul.name.tel for ul in userlist]
            for tel in tellist:
                SendSms().send(tel, subject)
            userlist = AlarmList.objects.filter(group=ag_obj, dd_status=1).filter(
                Q(name__app__name=appname) | Q(name__app__name='all')).distinct()
            ddlist = [ul.name.dd for ul in userlist]
            messages = {}
            body = {}
            form = []
            messages["message_url"] = cfg.get('dingding', 'url') + "/%s" % zr.id
            messages["pc_message_url"] = cfg.get('dingding', 'pc_url') + "/%s" % zr.id
            messages["head"] = {
                "bgcolor": "DBE97659",  # 前两位表示透明度
                "text": u"服务器故障"
            }
            body["title"] = subject
            body["content"] = content[5]
            form.append({'key': u'[故障主机]:', 'value': content[2]})
            form.append({'key': u'[故障时间]:', 'value': content[3]})
            form.append({'key': u'[事件ID]:', 'value': content[4]})
            body['form'] = form
            body["author"] = u"来自深圳运维监控系统"
            messages['body'] = body
            SendDingding().send(agentid=cfg.get('dingding', 'agentid'), userid='|'.join(ddlist), message=message,
                                messages=messages)
            userlist = AlarmList.objects.filter(group=ag_obj, tel_status=1).filter(
                Q(name__app__name=appname) | Q(name__app__name='all')).distinct()
            for u in userlist:
                if u.tel_status == 1:
                    SendMobile().send(message)
                elif ag_obj.tel_status == 2:
                    SendMobile().send(content, type='linkedsee_zhoujie')
            return HttpResponse("ok")
        else:
            userlist = AlarmList.objects.filter(group=ag_obj, weixin_status=1)
            wxlist = [wx.name.email for wx in userlist]
            SendWeixin().send('|'.join(wxlist), message, serial)
            userlist = AlarmList.objects.filter(group=ag_obj, email_status=1)
            emaillist = [ul.name.email for ul in userlist]
            SendMail().send(subject, emaillist, message)
            userlist = AlarmList.objects.filter(group=ag_obj, sms_status=1)
            tellist = [ul.name.tel for ul in userlist]
            for tel in tellist:
                SendSms().send(tel, subject)
            userlist = AlarmList.objects.filter(group=ag_obj, tel_status=1)
            for u in userlist:
                if u.tel_status == 1:
                    SendMobile().send(message)
                elif ag_obj.tel_status == 2:
                    SendMobile().send(content, type='linkedsee_zhoujie')
            return HttpResponse("ok")
    return HttpResponse("error")


def api(request, method):
    token = request.GET.get('token', '')
    if request.method == 'POST' and TokenAuth.objects.filter(token=token):
        name = TokenAuth.objects.get(token=token).name
        level = request.POST.get('level', '')
        subject = request.POST.get('subject', 'Default Subject...')
        content = request.POST.get('content', '')
        temp_reveiver = request.POST.get('receiverlist', '').split(',')
        sinal_alarmlist = AlarmList.objects.filter(group=AlarmGroup.objects.filter(id=6).first())
        if method == 'sendmail':
            receiverlist = []
            for receiver in temp_reveiver:
                if sinal_alarmlist.filter(name__email=receiver).filter(email_status=1):
                    receiverlist.append(receiver)
                    AlarmRecord.objects.create(type=u'邮件', name=name, token=token, subject=subject, receiver=receiver,
                                               content=content, level=level)
            SendMail().send(subject, receiverlist, content)
        if method == 'sendweixin':
            serial = request.POST.get('serial', '')
            for receiver in temp_reveiver:
                if sinal_alarmlist.filter(name__email=receiver).filter(weixin_status=1):
                    SendWeixin().send(receiver, content, serial)
                    AlarmRecord.objects.create(type=u'微信', name=name, token=token, serial=serial, receiver=receiver,
                                               content=content, level=level)
        if method == 'sendsms':
            mobiles = request.POST.get('mobiles', '').split(',')
            for m in mobiles:
                if sinal_alarmlist.filter(name__tel=m).filter(sms_status=1):
                    SendSms().send(m, content)
                    AlarmRecord.objects.create(type=u'短信', name=name, token=token, receiver=m, content=content,
                                               level=level)
        if method == 'sendmobile':
            type = request.POST.get('type', '')
            if sinal_alarmlist.filter(name__name=name).filter(tel_status=1):
                SendMobile().send(content, type)
                if type != 'linkedsee_zhoujie':
                    type = 'linkedsee_szyw'
                AlarmRecord.objects.create(type=u'电话', name=name, token=token,
                                           receiver=type, content=content, level=level)
        if method == 'senddingding':
            pass

        if method == 'sendgroup' and AlarmGroup.objects.filter(id=request.POST.get('groupid', '')):
            groupid = request.POST.get('groupid', '')
            group_obj = AlarmGroup.objects.get(id=groupid)
            group_alarmlist = AlarmList.objects.filter(group=group_obj)
            AlarmRecord.objects.create(type=u'公共组', name=name, token=token, subject=subject, receiver=groupid,
                                       content=content, level=level)
            receiverlist = []
            for receiver in temp_reveiver:
                if sinal_alarmlist.filter(name__email=receiver).filter(email_status=1):
                    receiverlist.append(receiver)
            group_alarmlist = group_alarmlist.filter(email_status=1)
            for u in group_alarmlist:
                if u.name.email not in receiverlist:
                    receiverlist.append(u.name.email)
            SendMail().send(subject, receiverlist, content)
            for receiver in temp_reveiver:
                if sinal_alarmlist.filter(name__email=receiver).filter(weixin_status=1):
                    SendWeixin().send(receiver, content, serial)
            group_alarmlist = group_alarmlist.filter(weixin_status=1)
            for u in group_alarmlist:
                if u.name.email not in receiverlist:
                    SendWeixin().send(receiver, content, serial)
            mobiles = request.POST.get('mobiles', '').split(',')
            for m in mobiles:
                if sinal_alarmlist.filter(name__tel=m).filter(sms_status=1):
                    SendSms().send(m, content)
            group_alarmlist = group_alarmlist.filter(sms_status=1)
            for u in group_alarmlist:
                if u.name.tel not in receiverlist:
                    SendSms().send(m, content)
        return HttpResponse("ok")
    return HttpResponse("error")


@login_required()
@permission_verify()
def tokenlist(request):
    temp_name = "skapi/api-header.html"
    obj_info = TokenAuth.objects.all()
    return render_to_response('skapi/tokenlist.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def tokenadd(request):
    temp_name = "skapi/api-header.html"
    if request.method == "POST":
        obj_form = TokenAuthForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = TokenAuthForm()
    return render_to_response('skapi/tokenadd.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def tokendel(request):
    id = request.GET.get('id', '')
    if id:
        TokenAuth.objects.get(id=id).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def alarmapirecord(request):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmRecord.objects.all()
    return render_to_response('skapi/alarmapirecord.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def alarmapidetail(request, ids):
    temp_name = "skapi/api-header.html"
    obj = get_object(AlarmRecord, id=ids)
    af = AlarmRecordForm(instance=obj)
    return render_to_response('skapi/alarmapidetail.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def alarmlogrecord(request):
    temp_name = "skapi/api-header.html"
    obj_info = ZabbixRecord.objects.all()[0:200]
    return render_to_response('skapi/alarmlogrecord.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def alarmlogdetail(request, ids):
    temp_name = "skapi/api-header.html"
    obj = get_object(ZabbixRecord, id=ids)
    af = ZabbixRecordForm(instance=obj)
    return render_to_response('skapi/alarmapidetail.html', locals(), RequestContext(request))


def ddlogdetail(request, ids):
    obj = get_object(ZabbixRecord, id=ids)
    return render_to_response('skapi/ddlogdetail.html', locals(), RequestContext(request))
