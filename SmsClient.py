# -*- coding: utf-8 -*-
import base64
import hmac
import hashlib
import json
import urllib
import urllib2
from datetime import datetime as dt
from hashlib import sha1

from config import APP_ID, APP_SECRET, GRANT_TYPE
from logger import Logger

TEMPLATE_ID = '91548711'
TEMPLATE_PARAM = {"orderCode": "8888888",
                  "times": "7",
                  "lessonUrl": "http://open.189.cn"
                  }


def get_access_token():
    url = 'https://oauth.api.189.cn/emp/oauth2/v3/access_token'
    param = {'grant_type': GRANT_TYPE, 'app_id': APP_ID, 'app_secret': APP_SECRET}
    param = urllib.urlencode(param)
    req = urllib2.Request(url, param)
    response = urllib2.urlopen(req).read()
    result = json.loads(response)
    if result['res_code'] == '0':
        Logger.info(result)
        return result['access_token']
    else:
        Logger.error(result)


ACCESS_TOKEN = get_access_token()


def get_time_stamp():
    timestamp = dt.now().year, dt.now().month, dt.now().day, dt.now().hour, dt.now().minute, dt.now().second
    timestamp = "%s-%s-%s %s:%s:%s" % timestamp
    return timestamp

def send_sms(template_id, template_param, acceptor_tel):
    '''
    :param template_id: 模版短信 ID
    :param template_param: 模版短信参数,字典类型
    :param acceptor_tel: 接收方号码,不支持0打头的号码
    :return: 成功返回短信唯一表示, 错误打印 log
    '''
    url = 'http://api.189.cn/v2/emp/templateSms/sendSms'
    timestamp = get_time_stamp()
    param = {'app_id': APP_ID,
             'access_token': ACCESS_TOKEN,
             'acceptor_tel': acceptor_tel,
             'template_id': template_id,
             'template_param': template_param,
             'timestamp': timestamp,
             }
    param = urllib.urlencode(param)
    req = urllib2.Request(url, param)
    response = urllib2.urlopen(req).read()
    result = json.loads(response)
    if result['res_code'] == 0:
        Logger.info(result)
        return result['identifier']
    else:
        Logger.error(result)


def msg_status(identifier):
    url = 'http://api.189.cn/v2/EMP/nsagSms/appnotify/querysmsstatus'
    timestamp = get_time_stamp()
    # param = {'access_token': ACCESS_TOKEN, 'app_id': APP_ID, 'identifier': identifier,'timestamp': timestamp}
    message = 'access_token=%s&app_id=%s&identifier=%s&timestamp=%s' % (ACCESS_TOKEN, APP_ID, identifier, timestamp)
    message = bytes(message).encode('utf-8')
    secret = bytes(APP_SECRET).encode('utf-8')
    sign = base64.b64encode(hmac.new(message, secret, digestmod=hashlib.sha1).digest())
    print message, sign
    param = {'access_token': ACCESS_TOKEN,
             'app_id': APP_ID,
             'identifier': identifier,
             'timestamp': timestamp,
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


def main():
    # identifier = send_sms(template_id=TEMPLATE_ID, template_param=TEMPLATE_PARAM, acceptor_tel='18801494967')
    # print identifier
    identifier = '90610411153526019157'
    msg_status(identifier)


if __name__ == '__main__':
    main()
