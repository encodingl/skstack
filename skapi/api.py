# -*- coding:utf-8 -*-
from django.core.mail import send_mail
from lib.com import config, cfg
import requests, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

import logging
log = logging.getLogger('api')


class SendMail:
    def __init__(self):
        self._from = 'Monitor<monitor.sz@mljr.com>'

    def send(self, subject, receiverlist, message):
        cfg = config()
        if cfg.get('api', 'email_status') == 'On':
            try:
                send_mail(subject, message, self._from, receiverlist, fail_silently=False)
                log.info(
                    '[邮件信息发送成功]:' + '[标题:' + subject + ']' + '[收件人:' + ','.join(
                        receiverlist) + ']' + '[内容:' + message + ']')
            except Exception, msg:
                log.error(msg)
        else:
            log.warning("邮件功能未开启.")


class SendWeixin:
    def __init__(self):
        self._CropID = cfg.get('api', 'weixin_cropid')
        self._Secret = cfg.get('api', 'weixin_secret')
        self._Gurl = "%s?corpid=%s&corpsecret=%s" % (cfg.get('api', 'weixin_gurl'), self._CropID, self._Secret)

    def send(self, receiver, message, serial, toparty=''):
        cfg = config()
        if cfg.get('api', 'weixin_status') == 'On':
            body = {
                "touser": receiver,
                "toparty": toparty,
                "msgtype": "text",
                "agentid": serial,
                "text": {
                    "content": message
                }
            }
            try:
                r = requests.get(self._Gurl)
                token = r.json()['access_token']
                Purl = "%s?access_token=%s" % (cfg.get('api', 'weixin_purl'), token)
                requests.post(Purl, data=json.dumps(body))
                log.info(
                    '[微信信息发送成功]:' + '[编号:' + serial + ']' + '[收件人:' + receiver + ']' + '[内容:' + message + ']')
            except Exception, msg:
                log.error(msg)
        else:
            log.warning("微信功能未开启.")


class SendSms:
    def __init__(self):
        self._url = cfg.get('api', 'sms_api')

    def send(self, mobile, message):
        cfg = config()
        if cfg.get('api', 'sms_status') == 'On':
            message = {
                "msg": '''{'content':'%s','mobile':'%s','bussdepartment':'zabbix','source':'zabbix','type':1}''' % (
                    message, mobile)
            }
            try:
                requests.get(self._url, message)
                log.info('[短信信息发送成功]:' + '[收件人:' + mobile + ']' + '[内容:' + message['msg'] + ']')
            except Exception, msg:
                log.error(msg)
        else:
            log.warning("短信功能未开启.")


class SendMobile:
    def __init__(self):
        self._url = cfg.get('api', 'linkedsee_api')
        self._token = cfg.get('api', 'szyw_token')

    def send(self, content, type='linkedsee_szyw'):
        cfg = config()
        if cfg.get('api', 'tel_status') == 'On':
            if type == 'linkedsee_zhoujie':
                self._token = cfg.get('api', 'zhoujie_token')
            headers = {
                'servicetoken': self._token
            }
            message = "{content:'%s'}" % content
            try:
                requests.post(self._url, message, headers=headers)
                log.info('[电话信息发送成功]:' + '[token:' + self._token + ']' + '[内容:' + message + ']')
            except Exception, msg:
                log.error(msg)
        else:
            log.warning("电话功能未开启.")


class SendDingding:
    def __init__(self):
        self.__params = {
            'corpid': cfg.get('dingding', 'corpid'),
            'corpsecret': cfg.get('dingding', 'corpsecret')
        }
        self.url_get_token = cfg.get('dingding', 'url_get_token')
        self.url_send = cfg.get('dingding', 'url_send')
        self.__token = self.__get_token()
        self.__token_params = {
            'access_token': self.__token
        }

    def __raise_error(self, res):
        raise Exception('error code: %s,error message: %s' % (res.json()['errcode'], res.json()['errmsg']))

    def __get_token(self):
        headers = {'content-type': 'application/json'}
        res = requests.get(self.url_get_token, headers=headers, params=self.__params)
        try:
            return res.json()['access_token']
        except:
            self.__raise_error(res)

    def send(self, agentid='', messages='', userid='', toparty='',message=''):
        cfg = config()
        if cfg.get('api', 'dd_status') == 'On':
            payload = {
                'touser': userid,
                'toparty': toparty,
                'agentid': agentid,
                'msgtype': 'oa',
                'oa': messages
            }
            headers = {'content-type': 'application/json'}
            params = self.__token_params
            try:
                requests.post(self.url_send, headers=headers, params=params, data=json.dumps(payload))
                log.info('[钉钉信息发送成功]:' + '[ 接收用户ID:' + userid + ']' + '[内容:' + message + ']')
            except Exception, msg:
                log.error(msg)
        else:
            log.warning("钉钉功能未开启.")
