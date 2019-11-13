import config.cookie as cookieConfig
import requests
import threading
import time
 
exitFlag = 0

name = 'test'
headers = cookieConfig.config['175']
resp = requests.post('https://hsc.jd.com/couponObtain/obtain',
    data = {
        'couponCode' : '0117251ef0b44fac885f59f3497d4095',
        'p' : '2',
        'pageClickKey' : '-1',
        'userArea' : '-1',
        'eid' : 'OJIHHJS4A3CEZRTHIS2ZC2OYM2OXGJTCUJYS5SMP7U4FYUPQUVEA2R7AXBWHRQGUFTQPOK3XSGZDWPTKXYGYJ6CVVA',
    },
    headers = headers
)
print ("%s: %s [%s]" % (name, time.ctime(time.time()), resp.json()))


# threads = []
# # 创建新线程
# i = 1
# for name, headers in cookieConfig.config.items():
#     thread = jdThread(i, "B-" + str(i) + ' ' + name, headers)
#     thread.start()
#     threads.append(thread)
#     i += 1
    
#     pass

# # 等待所有线程完成
# for t in threads:
#     t.join()
# print ("销毁原型机")