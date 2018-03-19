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
from aliyunsdkdyvmsapi.request.v20170525 import SingleCallByVoiceRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider

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

    def send(self, agentid='', messages='', userid='', toparty='', message=''):
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
                log.info(u'[钉钉信息发送成功][接收用户ID:%s][内容:%s]' % (userid, message))
            except Exception, msg:
                log.error(msg)
        else:
            log.warning(u"钉钉功能未开启.")


class AliyunMobile:
    def __init__(self):
        self.__business_id = uuid.uuid1()
        self.tts_code = cfg.get('aliyun', 'tts_code')
        self.show_number = cfg.get('aliyun', 'show_number')
        self.REGION = cfg.get('aliyun', 'region')
        self.PRODUCT_NAME = cfg.get('aliyun', 'product_name')
        self.DOMAIN = cfg.get('aliyun', 'domain')
        self.ACCESS_KEY_ID = cfg.get('aliyun', 'access_key_id')
        self.ACCESS_KEY_SECRET = cfg.get('aliyun', 'access_key_secret')
        self.acs_client = AcsClient(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, self.REGION)
        region_provider.add_endpoint(self.PRODUCT_NAME, self.REGION, self.DOMAIN)

    def tts_call(self, called_number, tts_param=None):
        ttsRequest = SingleCallByTtsRequest.SingleCallByTtsRequest()
        ttsRequest.set_TtsCode(self.tts_code)
        ttsRequest.set_OutId(self.__business_id)
        ttsRequest.set_CalledNumber(called_number)
        ttsRequest.set_CalledShowNumber(self.show_number)
        if tts_param is not None:
            ttsRequest.set_TtsParam(tts_param)
        try:
            ttsResponse = self.acs_client.do_action_with_exception(ttsRequest)
            log.info(u'[阿里云tts电话发送成功][接收用户ID:%s][show_number:%s][tts_code:%s][tts_param:%s]' % (
            called_number, self.show_number, self.tts_code, tts_param))
            return ttsResponse
        except Exception, e:
            log.error(e)
            return None

    def voice_call(self, called_number, voice_code):
        voiceRequest = SingleCallByVoiceRequest.SingleCallByVoiceRequest()
        voiceRequest.set_VoiceCode(voice_code)
        voiceRequest.set_OutId(self.__business_id)
        voiceRequest.set_CalledNumber(called_number)
        voiceRequest.set_CalledShowNumber(self.show_number)
        try:
            voiceResponse = self.acs_client.do_action_with_exception(voiceRequest)
            log.info(u'[阿里云voice电话发送成功][接收用户ID:%s][show_number:%s][voice_code:%s]' % (
            called_number, self.show_number, voice_code))
            return voiceResponse
        except Exception, e:
            log.error(e)
            return None
