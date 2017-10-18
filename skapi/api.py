# -*- coding:utf-8 -*-
from django.core.mail import send_mail
import requests, json
import logging

from skapi.models import AlarmStatus


class sendMail:
    def __init__(self, subject, receiverlist, message):
        self._from = 'Monitor<monitor.sz@mljr.com>'
        self._subject = subject
        self._receiverlist = receiverlist
        self._message = message
    def send(self):
        if AlarmStatus.objects.get(id=1).email_status:
            try:
                send_mail(self._subject, self._message, self._from, self._receiverlist, fail_silently=False)
            except Exception, e:
                logging.error("[邮件发送失败]:" + e.message())
        else:
            logging.warning("邮件功能未开启.")


class sendWeixin:
    def __init__(self, receiver, message, serial):
        self._CropID = "wxf97f43cc98f403ec"
        self._Secret = "bypQWOXYsytWQJBXu1Q9omb2O6rwp7G1bUK8V-94J32cKvjnD2PLhezvhlW1mvYj"
        self._Gurl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (
            self._CropID, self._Secret)
        self._body = {
            "touser": receiver,
            "toparty": "",
            "msgtype": "text",
            "agentid": serial,
            "text": {
                "content": message
            }
        }
    def send(self):
        if AlarmStatus.objects.get(id=1).weixin_status:
            try:
                r = requests.get(self._Gurl)
                token = r.json()['access_token']
                Purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token
                requests.post(Purl, data=json.dumps(self._body))
            except Exception, e:
                logging.error("[微信发送失败]:" + e.message())
        else:
            logging.warning("微信功能未开启.")


class sendSms:
    def __init__(self, mobile, message):
        self._url = 'http://notify.yyfq.com/notify/sms/single/send'
        self._message = {
            "msg": '''{'content':'%s','mobile':'%s','bussdepartment':'zabbix','source':'zabbix','type':1}''' % (
                message, mobile)
        }
    def send(self):
        if AlarmStatus.objects.get(id=1).sms_status:
            try:
                requests.get(self._url, self._message)
            except Exception, e:
                logging.error("[短信发送失败]:" + e.message())
        else:
            logging.warning("短信功能未开启.")

class sendMobile:
    def __init__(self, message, type='linkedsee_szyw'):
        self._url = 'http://www.linkedsee.com/alarm/zabbix'
        self._token = 'a138538e6f2cc8596901c2d26d89b279'
        if type == 'linkedsee_zhoujie':
            self._token = '21788f6aeb09ddb6cdad29da903dfd0d'
        self._headers = {
            'servicetoken': self._token
        }
        self._message = "{content:'%s'}" % message
    def send(self):
        if AlarmStatus.objects.get(id=1).tel_status:
            try:
                requests.post(self._url, self._message, headers=self._headers)
            except Exception, e:
                logging.error("[电话告警发送失败]:" + e.message())
        else:
            logging.warning("电话功能未开启.")


class sendDingding:
    '''待开发...'''
    pass
