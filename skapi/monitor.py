# coding:utf8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from skaccounts.permission import permission_verify

from models import AlarmUser, AlarmGroup, AlarmList, TokenAuth
from skapi.api import sendWeixin, sendMail, sendSms, sendMobile
from skapi.forms import AlarmUserForm, AlarmGroupForm, AlarmListForm, AddAlarmUserForm, TokenAuthForm
from lib.com import get_object, config, cfg, config_path
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
    obj_info = AlarmUser.objects.all()
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
    obj_info = AlarmGroup.objects.all()
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
        fp = open(config_path, 'w')
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

    return render_to_response('skapi/setup.html', locals(), RequestContext(request))


def zabbixalart(request):
    subject = request.POST.get('subject', '')
    content = request.POST.get('content', '')
    token = request.GET.get('token', '')
    type= request.GET.get('type', '')
    if request.method == 'POST' and token == cfg.get('token', 'token'):
        log.info('[token:' + token + ']' + '[subject:' + subject + ']' + '[content:' + content + ']')
        if type == 'appname':
            sub_data = subject.split(',', 2)
            groupid = int(sub_data[0])
            appname = sub_data[1]
            subject = sub_data[2]
            ag_obj = AlarmGroup.objects.get(id=groupid)
            serial = ag_obj.serial
            userlist = AlarmList.objects.filter(group=ag_obj, weixin_status=1).filter(name__app__name__contains=appname)
            for wx in userlist:
                message = u'[通知标题]:%s\n[收件人]:%s\n[通知内容]:\n%s' % (subject, wx.name.email, content)
                sendWeixin(wx.name.email, message, serial).send()
            userlist = AlarmList.objects.filter(group=ag_obj, email_status=1).filter(name__app__name__contains=appname)
            emaillist = [ul.name.email for ul in userlist]
            sendMail(subject, emaillist, content).send()
            userlist = AlarmList.objects.filter(group=ag_obj, sms_status=1).filter(name__app__name__contains=appname)
            tellist = [ul.name.tel for ul in userlist]
            for tel in tellist:
                sendSms(tel, content).send()
            if ag_obj.tel_status == 1:
                sendMobile(content).send()
            elif ag_obj.tel_status == 2:
                sendMobile(content, type='linkedsee_zhoujie').send()
            return HttpResponse("ok")
        else:
            sub_data = subject.split(',', 1)
            groupid = int(sub_data[0])
            subject = sub_data[1]
            ag_obj = AlarmGroup.objects.get(id=groupid)
            serial = ag_obj.serial
            userlist = AlarmList.objects.filter(group=ag_obj, weixin_status=1)
            for wx in userlist:
                message = u'[通知标题]:%s\n[收件人]:%s\n[通知内容]:\n%s' % (subject, wx.name.email, content)
                sendWeixin(wx.name.email, message, serial).send()
            userlist = AlarmList.objects.filter(group=ag_obj, email_status=1)
            emaillist = [ul.name.email for ul in userlist]
            sendMail(subject, emaillist, content).send()
            userlist = AlarmList.objects.filter(group=ag_obj, sms_status=1)
            tellist = [ul.name.tel for ul in userlist]
            for tel in tellist:
                sendSms(tel, content).send()
            if ag_obj.tel_status == 1:
                sendMobile(content).send()
            elif ag_obj.tel_status == 2:
                sendMobile(content, type='linkedsee_zhoujie').send()
            return HttpResponse("ok")
    return HttpResponse("error")


def api(request, method):
    token = request.GET.get('token', '')
    if request.method == 'POST' and TokenAuth.objects.filter(token=token):
        if method == 'sendmail':
            level = request.POST.get('level', '')
            subject = request.POST.get('subject', 'Default Subject...')
            receiverlist = request.POST.get('receiverlist', '').split(',')
            content = request.POST.get('content', '')
            sendMail(subject, receiverlist, content).send()
        if method == 'sendweixin':
            level = request.POST.get('level', '')
            receiverlist = request.POST.get('receiverlist', '').split(',')
            content = request.POST.get('content', '')
            serial = request.POST.get('serial', '')
            for receiver in receiverlist:
                sendWeixin(receiver, content, serial).send()
        if method == 'sendsms':
            level = request.POST.get('level', '')
            mobiles = request.POST.get('mobiles', '').split(',')
            content = request.POST.get('content', '')
            for mobile in mobiles:
                sendSms(mobile, content).send()
        if method == 'sendmobile':
            level = request.POST.get('level', '')
            type = request.POST.get('type', '')
            content = request.POST.get('content', '')
            sendMobile(content, type).send()
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
