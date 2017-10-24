# -*- coding:utf-8 -*-
from django.core.mail import send_mail
import requests, json
import logging
from lib.com import config, cfg


class sendMail:
    def __init__(self, subject, receiverlist, message):
        self._from = 'Monitor<monitor.sz@mljr.com>'
        self._subject = subject
        self._receiverlist = receiverlist
        self._message = message

    def send(self):
        cfg = config()
        if cfg.get('api', 'email_status') == 'On':
            try:
                send_mail(self._subject, self._message, self._from, self._receiverlist, fail_silently=False)
            except Exception, e:
                logging.error("[邮件发送失败]:" + e.message())
        else:
            logging.warning("邮件功能未开启.")


class sendWeixin:
    def __init__(self, receiver, message, serial):
        self._CropID = cfg.get('api', 'weixin_cropid')
        self._Secret = cfg.get('api', 'weixin_secret')
        self._Gurl = "%s?corpid=%s&corpsecret=%s" % (cfg.get('api', 'weixin_gurl'), self._CropID, self._Secret)
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
        cfg = config()
        if cfg.get('api', 'weixin_status') == 'On':
            try:
                r = requests.get(self._Gurl)
                token = r.json()['access_token']
                Purl = "%s?access_token=%s" % (cfg.get('api', 'weixin_purl'),token)
                requests.post(Purl, data=json.dumps(self._body))
            except Exception, e:
                logging.error("[微信发送失败]:" + e.message())
        else:
            logging.warning("微信功能未开启.")


class sendSms:
    def __init__(self, mobile, message):
        self._url = cfg.get('api', 'sms_api')
        self._message = {
            "msg": '''{'content':'%s','mobile':'%s','bussdepartment':'zabbix','source':'zabbix','type':1}''' % (
                message, mobile)
        }

    def send(self):
        cfg = config()
        if cfg.get('api', 'sms_status') == 'On':
            try:
                requests.get(self._url, self._message)
            except Exception, e:
                logging.error("[短信发送失败]:" + e.message())
        else:
            logging.warning("短信功能未开启.")


class sendMobile:
    def __init__(self, message, type='linkedsee_szyw'):
        self._url = cfg.get('api', 'linkedsee_api')
        self._token = cfg.get('api', 'linkedsee_token_szyw')
        if type == 'linkedsee_zhoujie':
            self._token = cfg.get('api', 'linkedsee_token_zhoujie')
        self._headers = {
            'servicetoken': self._token
        }
        self._message = "{content:'%s'}" % message

    def send(self):
        cfg = config()
        if cfg.get('api', 'tel_status') == 'On':
            try:
                requests.post(self._url, self._message, headers=self._headers)
            except Exception, e:
                logging.error("[电话告警发送失败]:" + e.message())
        else:
            logging.warning("电话功能未开启.")


class sendDingding:
    '''待开发...'''
    pass
