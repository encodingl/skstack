# coding:utf8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from skaccounts.permission import permission_verify
from models import AlarmGroup, AlarmList, TokenAuth, AlarmRecord, ZabbixRecord, LevelPolicy, ApiRecord
from skapi.api import SendWeixin, SendMail, SendDingding
from skapi.forms import AlarmGroupForm, AlarmListForm, TokenAuthForm, \
    AlarmRecordForm, ZabbixRecordForm, LevelPolicyForm, ApiRecordForm
from lib.com import get_object, config, configfile
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
    if request.method == 'POST':
        token = request.GET.get('token', '')
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

        if not ag or not ag.tokens.filter(token=token).first():
            return HttpResponse("error")

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

        if content[1].split(':')[1] == 'OK':
            subject = u'[告警恢复通知]:%s' % subject
        elif content[1].split(':')[1] == 'PROBLEM':
            subject = u'[告警故障通知]:%s' % subject

            aliyun = AliyunAPI()
            smslist = [ul.user.tel for ul in sms_user_obj]
            params = "{\"code\":\"98123\",\"remark\":\"%s\"}" % subject
            aliyun.send_sms(','.join(smslist), params, 'sms_code1')

            for tel in tel_user_obj:
                aliyun.tts_call(tel.user.tel, params, 'tts_code1')

        ddlist = [ul.user.dd for ul in dd_user_obj]
        SendDingding().send(subject, content, userid='|'.join(ddlist), logid=logid)

        return HttpResponse("ok")
    return HttpResponse("error")


@csrf_exempt
def api(request, method):
    if request.method == 'POST':
        msg = {'Code': 'Error'}

        token = request.GET.get('token', '').strip()
        groupid = request.POST.get('groupid', '').strip()
        policy = request.POST.get('policy', '').strip()
        level = request.POST.get('level', '').strip()
        subject = request.POST.get('subject', 'Default Subject YYFQ Alart!').strip()
        content = request.POST.get('content', '').strip()

        if '' in [groupid, content]:
            msg['Message'] = u'参数错误:groupid,content字段不能为空!'
            return HttpResponse(dumps(msg))

        if not groupid.isdigit():
            msg['Message'] = u'参数错误:groupid 必须是纯数字!'
            return HttpResponse(dumps(msg))

        ag = AlarmGroup.objects.get(id=groupid)
        if not ag:
            msg['Message'] = '分组ID不存在,请联系运维人员!'
            return HttpResponse(dumps(msg))
        if not ag.tokens.filter(token=token).first():
            msg['Message'] = u'你的Token没有权限,请联系运维!'
            return HttpResponse(dumps(msg))

        name = TokenAuth.objects.get(token=token).name

        if method == 'sendbygroup':
            if policy:
                _policy = [p.strip() for p in policy.split(',')]
                for p in _policy:
                    if p not in Alarm_TYPE_Code:
                        msg['Message'] = '参数错误:策略参数不存在!'
                        return HttpResponse(dumps(msg))
            else:
                if level not in Log_Type:
                    msg['Message'] = u'如果不指定策略,level参数错误!'
                    return HttpResponse(dumps(msg))
                if not ag.levelpolicy:
                    msg['Message'] = u'没有授权日志策略,请联系运维授权!'
                    return HttpResponse(dumps(msg))

            logid = ''
            if config().get('record', 'api_status') == 'On':
                zr = ApiRecord.objects.create(name=name, groupid=groupid, token=token, subject=subject,
                                              content=content, level=level, policy=policy)
                logid = zr.id

            alarmList = ag.alarmlist_set.all()

            email_user_obj = alarmList.filter(email_status=1)
            emaillist = [u.user.email for u in email_user_obj]

            wx_user_obj = alarmList.filter(weixin_status=1)
            wxlist = [wx.user.email for wx in wx_user_obj]

            dd_user_obj = alarmList.filter(dd_status=1)
            ddlist = [ul.user.dd for ul in dd_user_obj]

            sms_user_obj = alarmList.filter(sms_status=1)
            smslist = [u.user.tel for u in sms_user_obj]

            tel_user_obj = alarmList.filter(tel_status=1)
            tellist = [u.user.tel for u in tel_user_obj]

            aliyun = AliyunAPI()
            params = "{\"code\":\"98123\",\"remark\":\"%s\"}" % subject

            data = []
            if not _policy:
                exec ("data = ag.levelpolicy.%s_policy" % level)

            if '0' in data or 'email' in _policy:
                SendMail().send(subject, emaillist, content)
            if '1' in data or 'sms' in _policy:
                aliyun.send_sms(','.join(smslist), params, 'sms_code1')
            if '2' in data or 'weixin' in _policy:
                SendWeixin().send('|'.join(wxlist), content, ag.serial)
            if '3' in data or 'dingding' in _policy:
                SendDingding().send(subject, content, userid='|'.join(ddlist), logid=logid)
            if '4' in data or 'mobile' in _policy:
                for tel in tellist:
                    aliyun.tts_call(tel, params, 'tts_code1')

            msg['Message'] = u'请求成功!'
            msg['Code'] = 'OK'
            return HttpResponse(dumps(msg))
        else:
            sinal_alarmlist = AlarmList.objects.filter(group=AlarmGroup.objects.filter(id=6).first())
            temp_reveiver = [r.strip() for r in request.POST.get('reveivers', '').split(',')]
            if method == 'sendmail':
                receiverlist = []
                for receiver in temp_reveiver:
                    if sinal_alarmlist.filter(name__email=receiver).filter(email_status=1):
                        receiverlist.append(receiver)
                        AlarmRecord.objects.create(type=u'邮件', name=name, token=token, subject=subject,
                                                   receiver=receiver,
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
    obj_info = ApiRecord.objects.all()
    return render_to_response('skapi/alarmapirecord.html', locals(), RequestContext(request))


@login_required()
@permission_verify()
def alarmapidetail(request, ids):
    temp_name = "skapi/api-header.html"
    obj = get_object(ApiRecord, id=ids)
    af = ApiRecordForm(instance=obj)
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
