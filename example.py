from SmsClient import SmsClient
from config import APP_ID, APP_SECRET, GRANT_TYPE

TEMPLATE_ID = '91548711'
TEMPLATE_PARAM = {"orderCode": "demoday",
                  "times": "7",
                  "lessonUrl": "http://open.189.cn"
                  }

if __name__ == '__main__':
    sms = SmsClient(app_id=APP_ID,
                    app_secret=APP_SECRET,
                    grant_type=GRANT_TYPE
                    )
    sms.send_sms(TEMPLATE_ID, TEMPLATE_PARAM, '18801494967')
