import config.cookie as cookieConfig
import requests
import threading
import time
 
exitFlag = 0

name = 'test'
headers = cookieConfig.config['136']
resp = requests.post('https://hsc.jd.com/couponObtain/obtain',
    data = {
        'couponCode' : 'b8a3581b2d1f447d8184504a366ebaa9',
        'p' : '2',
        'pageClickKey' : '-1',
        'userArea' : '-1',
        'eid' : 'FZVIO7FBUDNUVGTEMH5TKAFP5QJ4PUMGWUQ6GHMTHVHCPES6LPPZWAD6JTZ4ZSDMTOWXPSEFYRFCHRNXPLW4GUWKL4',
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