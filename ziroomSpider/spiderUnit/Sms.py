import requests
import config.sms as smsConfig
from datetime import datetime
import hashlib

# 梦网sms的接口
class Sms(object):
    def __init__(self):
        self.uid = smsConfig.config['uid']
        self.pwd = smsConfig.config['pwd']
        self.ip = smsConfig.config['ip']

    def sendMsg(self, mobile, content):
        # 获取图片信息
        uid = self.uid
        pwd = self.pwd
        ip = self.ip
        now = datetime.now()
        signTime = now.strftime(r"%m%d%H%M%S")
        signPwdRaw = uid.upper() + '00000000' + pwd + signTime
        md5 = hashlib.md5()
        md5.update(signPwdRaw.encode('utf-8'))
        signPwd = md5.hexdigest()

        # print({
        #         'userid' : uid,
        #         'pwd' : signPwd,
        #         'mobile' : mobile,
        #         'content' : content.encode("GBK"),
        #         'timestamp' : signTime,
        #     })
        # print('http://' + ip + '/sms/v2/std/single_send')
        # return
        
        r = requests.post(
            'http://' + ip + '/sms/v2/std/single_send',
            data={
                'userid' : uid,
                'pwd' : signPwd,
                'mobile' : mobile,
                'content' : content.encode("GBK"),
                'timestamp' : signTime,
            }
        )
        return print(r.status_code)

        




