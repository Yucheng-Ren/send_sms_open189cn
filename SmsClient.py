# -*- coding: utf-8 -*-
import base64
import hmac
import hashlib
import json
import urllib
import urllib2
from datetime import datetime as dt
from logger import Logger


class SmsClient(object):
    """
    通过电信 API 发送短信
    """
    def __init__(self, app_id=None, app_secret=None, grant_type='client_credentials'):
        '''
        :param app_id: app_id 在电信app 控制台可以查询到
        :param app_secret: 同上
        :param grant_type: 授权方法,目前只写了 client_credentials
        :return:
        '''
        super(SmsClient, self).__init__()
        self.APP_ID = app_id
        self.APP_SECRET = app_secret
        self.GRANT_TYPE = grant_type

    def _get_time_stamp(self):
        timestamp = dt.now().year, dt.now().month, dt.now().day, dt.now().hour, dt.now().minute, dt.now().second
        timestamp = "%s-%s-%s %s:%s:%s" % timestamp
        return timestamp

    def _get_access_token(self):
        url = 'https://oauth.api.189.cn/emp/oauth2/v3/access_token'
        param = {'grant_type': self.GRANT_TYPE, 'app_id': self.APP_ID, 'app_secret': self.APP_SECRET}
        param = urllib.urlencode(param)
        req = urllib2.Request(url, param)
        response = urllib2.urlopen(req).read()
        result = json.loads(response)
        if result['res_code'] == '0':
            Logger.info(result)
            return result['access_token']
        else:
            Logger.error(result)

    def send_sms(self, template_id, template_param, acceptor_tel):
        '''
        :param template_id: 模版短信 ID
        :param template_param: 模版短信参数,字典类型
        :param acceptor_tel: 接收方号码,不支持0打头的号码
        :return: 成功返回短信唯一表示, 错误打印 log
        '''
        url = 'http://api.189.cn/v2/emp/templateSms/sendSms'
        param = {'app_id': self.APP_ID,
                 'access_token': self._get_access_token(),
                 'acceptor_tel': acceptor_tel,
                 'template_id': template_id,
                 'template_param': template_param,
                 'timestamp': self._get_time_stamp(),
                 }
        param = urllib.urlencode(param)
        req = urllib2.Request(url, param)
        response = urllib2.urlopen(req).read()
        result = json.loads(response)
        if result['res_code'] == 0:
            Logger.info(result)
            return result['idertifier']
        else:
            Logger.error(result)

    def send_sms_by_list(self, template_id, template_param, tel_list):
        '''
        按照列表群发
        :param template_id: 模版短信 ID
        :param template_param: 模版短信参数,字典类型
        :param tel_list: 接收方电话号码组成的 list
        :return: idertifier 组成的 list，idertifier 为电信返回的短信唯一标示
        '''
        result = []
        for tel in tel_list:
            iden = self.send_sms(template_id, template_param, tel)
            result.append(iden)
        return result

    def msg_status(self, identifier):
        url = 'http://api.189.cn/v2/EMP/nsagSms/appnotify/querysmsstatus'
        message = 'access_token=%s&app_id=%s&identifier=%s&timestamp=%s' % (self._get_access_token(), self.APP_ID, identifier, self._get_time_stamp())
        message = bytes(message).encode('utf-8')
        secret = bytes(self.APP_SECRET).encode('utf-8')
        sign = base64.b64encode(hmac.new(message, secret, digestmod=hashlib.sha1).digest())
        print message, sign
        param = {'access_token': self._get_access_token(),
                 'app_id': self.APP_ID,
                 'identifier': identifier,
                 'timestamp': self._get_time_stamp(),
                 'sign': sign,
                 }
        param = urllib.urlencode(param)
        req = urllib2.Request(url, param)
        response = urllib2.urlopen(req).read()
        result = json.loads(response)
        if result['res_code'] == '0':
            Logger.info(result)
        else:
            Logger.error(result)
