# coding:utf8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from skaccounts.permission import permission_verify
from models import AlarmUser, AlarmGroup, AlarmList, TokenAuth, UserPolicy, AlarmRecord, ZabbixRecord, ServiceType, \
    LevelPolicy
from skapi.api import SendWeixin, SendMail, SendSms, SendMobile, SendDingding
from skapi.forms import AlarmUserForm, AlarmGroupForm, AlarmListForm, AddAlarmUserForm, TokenAuthForm, UserPolicyForm, \
    AlarmRecordForm, ZabbixRecordForm, LevelPolicyForm, ServiceTypeForm
from lib.com import get_object, config, cfg, configfile
from lib.type import Alarm_TYPE_Code, Log_Type
from utils import initAlarmList
from api import AliyunAPI
import logging
from json import dumps

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
            obj_info = temp.alarmlist_set.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))


def alarmlistedit(request, ids):
    obj = AlarmList.objects.get(id=ids)
    status = 0
    if request.method == "POST":
        form = AlarmListForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
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
    obj_info = LevelPolicy.objects.all()
    return render_to_response('skapi/policy.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def policyadd(request):
    temp_name = "skapi/api-header.html"
    if request.method == "POST":
        obj_form = LevelPolicyForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = LevelPolicyForm()
    return render_to_response('skapi/policyadd.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def policydel(request):
    id = request.GET.get('id', '')
    if id:
        LevelPolicy.objects.get(id=id).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def policyedit(request, ids):
    temp_name = "skapi/api-header.html"
    status = 0
    obj = get_object(LevelPolicy, id=ids)
    if request.method == 'POST':
        af = LevelPolicyForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = LevelPolicyForm(instance=obj)
    return render_to_response('skapi/policyedit.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def servicetype(request):
    temp_name = "skapi/api-header.html"
    obj_info = ServiceType.objects.all()
    return render_to_response('skapi/servicetype.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def servicetypeadd(request):
    temp_name = "skapi/api-header.html"
    if request.method == "POST":
        obj_form = ServiceTypeForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = ServiceTypeForm()
    return render_to_response('skapi/servicetypeadd.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def servicetypedel(request):
    id = request.GET.get('id', '')
    if id:
        ServiceType.objects.get(id=id).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def servicetypeedit(request, ids):
    temp_name = "skapi/api-header.html"
    status = 0
    obj = get_object(ServiceType, id=ids)
    if request.method == 'POST':
        af = ServiceTypeForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = ServiceTypeForm(instance=obj)
    return render_to_response('skapi/servicetypeedit.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def grouplist(request):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmGroup.objects.order_by("-id")
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


@csrf_exempt
def zabbixalart(request):
    token = request.GET.get('token', '')
    if request.method == 'POST' and token == cfg.get('token', 'token'):
        groupid = request.POST.get('groupid', '')
        appname = request.POST.get('appname', '')
        type = request.POST.get('type', '')
        subject = request.POST.get('subject', '')
        content = request.POST.get('content', '').split('||')
        log.info('[token:%s][groupid:%s][appname:%s][type:%s][subject:%s][content:%s]' % (
            token, groupid, appname, type, subject, content))
        ag = AlarmGroup.objects.get(id=groupid)
        serial = ag.serial
        message = '\n'.join(content)
        logid = ''

        if config().get('record', 'zabbix_status') == 'On':
            zr = ZabbixRecord.objects.create(name=type, token=token, subject=subject, appname=appname,
                                             status=content[1].split(':', 1)[1],
                                             host=content[2].split(':', 1)[1], event=content[4].split(':', 1)[1],
                                             content=content[-1].split(':', 1)[1])
            logid = zr.id

        wx_user_obj = ag.alarmlist_set.filter(weixin_status=1)
        email_user_obj = ag.alarmlist_set.filter(email_status=1)
        sms_user_obj = ag.alarmlist_set.filter(sms_status=1)
        dd_user_obj = ag.alarmlist_set.filter(dd_status=1)
        tel_user_obj = ag.alarmlist_set.filter(tel_status=1)

        if appname != 'normal':
            wx_user_obj = wx_user_obj.filter(Q(app__name=appname) | Q(app__name='all')).distinct()
            email_user_obj = email_user_obj.filter(Q(app__name=appname) | Q(app__name='all')).distinct()
            sms_user_obj = sms_user_obj.filter(Q(app__name=appname) | Q(app__name='all')).distinct()
            dd_user_obj = dd_user_obj.filter(Q(app__name=appname) | Q(app__name='all')).distinct()
            tel_user_obj = tel_user_obj.filter(Q(app__name=appname) | Q(app__name='all')).distinct()

        wxlist = [wx.user.email for wx in wx_user_obj]
        SendWeixin().send('|'.join(wxlist), message, serial)

        emaillist = [ul.user.email for ul in email_user_obj]
        SendMail().send(subject, emaillist, message)

        if content[1] == 'OK':
            subject = u'[告警恢复通知]:%s' % subject
        elif content[1] == 'PROBLEM':
            subject = u'[告警故障通知]:%s' % subject

            aliyun = AliyunAPI()
            smslist = [ul.user.tel for ul in sms_user_obj]
            params = "{\"code\":\"98123\",\"remark\":\"%s\"}" % subject
            aliyun.send_sms(','.join(smslist), params, 'sms_code1')

            for tel in tel_user_obj:
                aliyun.tts_call(tel.user.tel, params, 'tts_code1')

        ddlist = [ul.user.dd for ul in dd_user_obj]
        messages = {}
        body = {}
        form = []
        messages["message_url"] = cfg.get('dingding', 'url') + "/%s" % logid
        messages["pc_message_url"] = cfg.get('dingding', 'pc_url') + "/%s" % logid
        messages["head"] = {
            "bgcolor": "DBE97659",  # 前两位表示透明度
            "text": u"服务器故障"
        }
        body["title"] = subject
        body["content"] = content[-1]
        for text in content[1:-1]:
            form.append({'key': u'', 'value': text})
        body['form'] = form
        body["author"] = u"来自深圳运维监控系统"
        messages['body'] = body
        SendDingding().send(agentid=cfg.get('dingding', 'agentid'), userid='|'.join(ddlist), message=message,
                            messages=messages)
        return HttpResponse("ok")
    return HttpResponse("error")


@csrf_exempt
def api(request, method):
    token = request.GET.get('token', '')
    if request.method == 'POST' and TokenAuth.objects.filter(token=token):
        name = TokenAuth.objects.get(token=token).name
        typecode = request.POST.get('typeCode', '').strip()
        policy = request.POST.get('policy', '').strip()
        level = request.POST.get('level', '').strip()
        subject = request.POST.get('subject', 'Default Subject...').strip()
        content = request.POST.get('content', '').strip()
        groupid = request.POST.get('groupid', '').strip()

        reveivers = [i.strip() for i in request.POST.get('receiverlist', '').split(',')]

        msg = {'Code': 'Error'}
        if method == 'sendbygroup':
            if '' in [groupid, content, type]:
                msg['Message'] = '参数错误!'
                return HttpResponse(dumps(msg))
            if policy:
                _policy = [p.strip() for p in policy.split(',')]
                for p in _policy:
                    if p not in Alarm_TYPE_Code:
                        msg['Message'] = '策略参数错误!'
                        return HttpResponse(dumps(msg))
                if not ServiceType.objects.filter(typecode=typecode):
                    msg['Message'] = '业务类型不存在,请联系运维人员!'
                    return HttpResponse(dumps(msg))

                alarmGroup = AlarmGroup.objects.filter(id=groupid).first()
                if not alarmGroup:
                    msg['Message'] = '分组ID不存在,请联系运维人员!'
                    return HttpResponse(dumps(msg))
                alarmList = AlarmList.objects.filter(group=alarmGroup)
                if 'mobile' in _policy:
                    tel_user_obj = alarmList.filter(tel_status=1)
                    aliyun = AliyunAPI()
                    params = "{\"code\":\"98123\",\"remark\":\"%s\"}" % subject
                    for tel in tel_user_obj:
                        aliyun.tts_call(tel.user.tel, params, 'tts_code1')

                if 'dingding' in _policy:
                    dd_user_obj = alarmList.filter(dd_status=1)

                if 'email' in _policy:
                    email_user_obj = alarmList.filter(email_status=1)
                    emaillist = [u.user.email for u in email_user_obj]
                    SendMail().send(subject, emaillist, content)

                if 'weixin' in _policy:
                    wx_user_obj = alarmList.filter(weixin_status=1)
                    wxlist = [wx.user.email for wx in wx_user_obj]
                    SendWeixin().send('|'.join(wxlist), content, alarmGroup.serial)

                if 'sms' in _policy:
                    sms_user_obj = alarmList.filter(sms_status=1)
                    aliyun = AliyunAPI()
                    smslist = [u.user.tel for u in sms_user_obj]
                    params = "{\"code\":\"98123\",\"remark\":\"%s\"}" % subject
                    aliyun.send_sms(','.join(smslist), params, 'sms_code1')
                msg['Message'] = '请求成功!'
                msg['Code'] = 'OK'
                return HttpResponse(dumps(msg))

            else:
                pass

                if level not in ['info', 'warn', 'error', 'fatal']:
                    msg['Message'] = 'level级别错误,请填写正确的级别名称!'
                    return HttpResponse(dumps(msg))

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

        if method == 'sendtel':
            results = []
            type = request.POST.get('type', u'有用分期')
            mobiles = [i.strip() for i in request.POST.get('mobiles', '').split(',')]
            params = "{\"code\":\"98123\",\"product\":\"%s\"}" % type
            aliyun = AliyunAPI()
            for mobile in mobiles:
                result = aliyun.tts_call(mobile, params)
                results.append(result)
                log.info(result)
            return HttpResponse(results)

        if method == 'sendsms':
            content = request.POST.get('content', u'无')
            mobiles = request.POST.get('mobiles', '')
            params = "{\"code\":\"98123\",\"remark\":\"%s\"}" % content
            aliyun = AliyunAPI()
            result = aliyun.send_sms(mobiles, params)
            log.info(result)
            return HttpResponse(result)

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
    obj_info = ZabbixRecord.objects.order_by('-id')[0:100]
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
