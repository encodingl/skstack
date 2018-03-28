# -*- coding:utf-8 -*-
from django.core.mail import send_mail
from lib.com import config, cfg
import requests, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from requests.packages.urllib3.exceptions import InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
from requests.packages.urllib3.exceptions import SNIMissingWarning

requests.packages.urllib3.disable_warnings(SNIMissingWarning)

from aliyunsdkdyvmsapi.request.v20170525 import SingleCallByTtsRequest
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid

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
                log.info(u'[邮件信息发送成功]:[标题:%s][收件人:%s][内容:%s]' % (subject, ','.join(receiverlist), message))
            except Exception, msg:
                log.error(msg)
        else:
            log.warning(u"邮件功能未开启.")


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
                    u'[微信信息发送成功]:[编号:%s][收件人:%s][内容:%s]' % (serial, receiver, message))
            except Exception, msg:
                log.error(msg)
        else:
            log.warning(u"微信功能未开启.")


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
                log.info(u'[短信信息发送成功]:[收件人:%s][内容:%s]' % (mobile, message['msg']))
            except Exception, msg:
                log.error(msg)
        else:
            log.warning(u"短信功能未开启.")


class SendMobile:
    def __init__(self):
        self._url = cfg.get('api', 'linkedsee_api')
        self._token = cfg.get('api', 'szyw_token')

    def send(self, content, type='linkedsee_szyw'):
        cfg = config()
        if cfg.get('api', 'tel_status') == 'On':
            if type == 'linkedsee_zhoujie':
                self._token = cfg.get('api', 'zhoujie_token')
            if type == 'linkedsee_mingai':
                self._token = cfg.get('api', 'mingai_token')
            headers = {
                'servicetoken': self._token
            }
            message = "{content:'%s'}" % content
            try:
                requests.post(self._url, message, headers=headers)
                log.info(u"[电话信息发送成功]:[token:%s][内容:%s][type:%s]" % (self._token, message, type))
            except Exception, msg:
                log.error(msg)
        else:
            log.warning(u"电话功能未开启.")


class SendDingding:
    def __init__(self):
        self.__params = {
            'corpid': cfg.get('dingding', 'corpid'),
            'corpsecret': cfg.get('dingding', 'corpsecret')
        }
        self.agentid = cfg.get('dingding', 'agentid')
        self.url_get_token = cfg.get('dingding', 'url_get_token')
        self.url_send = cfg.get('dingding', 'url_send')
        self.url = cfg.get('dingding', 'url')
        self.pc_url = cfg.get('dingding', 'pc_url')
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

    def send(self, subject, content, userid='', logid=-1, toparty=''):
        cfg = config()
        if cfg.get('api', 'dd_status') == 'On':

            messages = {}
            body = {}
            form = []
            messages["message_url"] = self.url + "/%s" % logid
            messages["pc_message_url"] = self.pc_url + "/%s" % logid
            messages["head"] = {
                "bgcolor": "DBE97659",  # 前两位表示透明度
                "text": u"服务器故障"
            }
            body["title"] = subject
            if isinstance(content, list):
                body["content"] = content[-1]
                for text in content[1:-1]:
                    form.append({'key': u'', 'value': text})
            else:
                body["content"] = content
            body['form'] = form
            body["author"] = u"来自深圳运维监控系统"
            messages['body'] = body

            payload = {
                'touser': userid,
                'toparty': toparty,
                'agentid': self.agentid,
                'msgtype': 'oa',
                'oa': messages
            }
            headers = {'content-type': 'application/json'}
            params = self.__token_params

            try:
                requests.post(self.url_send, headers=headers, params=params, data=json.dumps(payload))
                log.info(u'[钉钉信息发送成功][接收用户ID:%s][内容:%s]' % (userid, json.dumps(content)))
            except Exception, msg:
                log.error(msg)
        else:
            log.warning(u"钉钉功能未开启.")


class AliyunAPI:
    def __init__(self):
        self.__BUSINESS_ID = uuid.uuid1()
        self.SIGN_NAME = cfg.get('aliyun', 'sign_name')
        self.SHOW_NUMBER = cfg.get('aliyun', 'show_number')
        self.REGION = cfg.get('aliyun', 'region')
        self.ACCESS_KEY_ID = cfg.get('aliyun', 'access_key_id')
        self.ACCESS_KEY_SECRET = cfg.get('aliyun', 'access_key_secret')
        self.acs_client = AcsClient(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, self.REGION)

    def tts_call(self, called_number, params, tts_code='tts_code'):
        tts_code = cfg.get('aliyun', tts_code)
        ttsRequest = SingleCallByTtsRequest.SingleCallByTtsRequest()
        ttsRequest.set_TtsCode(tts_code)
        ttsRequest.set_OutId(self.__BUSINESS_ID)
        ttsRequest.set_CalledNumber(called_number)
        ttsRequest.set_CalledShowNumber(self.SHOW_NUMBER)
        if params is not None:
            ttsRequest.set_TtsParam(params)
        try:
            ttsResponse = self.acs_client.do_action_with_exception(ttsRequest)
            log.info(u'[阿里云tts电话发送成功][接收用户ID:%s][show_number:%s][tts_code:%s][params:%s]' % (
                called_number, self.SHOW_NUMBER, self.TTS_CODE, params))
            return ttsResponse
        except Exception, e:
            log.error(e)
            return u"请求异常!"

    def send_sms(self, called_number, params, sms_code='sms_code'):
        sms_code = cfg.get('aliyun', sms_code)
        smsRequest = SendSmsRequest.SendSmsRequest()
        smsRequest.set_TemplateCode(sms_code)
        if params is not None:
            smsRequest.set_TemplateParam(params)
        smsRequest.set_OutId(self.__BUSINESS_ID)
        smsRequest.set_SignName(self.SIGN_NAME)
        smsRequest.set_PhoneNumbers(called_number)
        try:
            smsResponse = self.acs_client.do_action_with_exception(smsRequest)
            log.info(u'[阿里云sms短信服务发送成功][接收用户ID:%s][sms_code:%s][params:%s]' % (
                called_number, self.SMS_CODE, params))

            return smsResponse
        except Exception, e:
            log.error(e)
            return u"请求异常!"
