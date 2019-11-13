import config.cookie as cookieConfig
import requests
import threading
import time
 
exitFlag = 0
 
class jdThread(threading.Thread):
    def __init__(self, threadID, name, headers, eid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.headers = headers
        self.eid = eid
    def run(self):
        print ("生成机体 " + self.name)
        getCoupon(self.name, self.headers, self.eid)
        print ("销毁机体 " + self.name)
 
def getCoupon(name, headers, eid):
    while 1:
        # 判断当前时间
        # time.sleep(0.05)
        t = (int)(time.time())
        if t < 1573646385:
            # 19:59:50
            print("%s: %s [%s]" % (name, time.ctime(time.time()), 'waiting'))
            continue
        if t > 1573646405:
            # 20:00:10
            print("%s: %s [%s]" % (name, time.ctime(time.time()), 'end'))
            return
        resp = requests.post('https://hsc.jd.com/couponObtain/obtain',
            data = {
                'couponCode' : '0117251ef0b44fac885f59f3497d4095',
                'p' : '2',
                'pageClickKey' : '-1',
                'userArea' : '-1',
                'eid' : eid,
            },
            headers = headers
        )
        print ("%s: %s [%s]" % (name, time.ctime(time.time()), resp.json()))

threads = []
# 创建新线程
i = 1
for name, headers in cookieConfig.config.items():
    n = 10
    counter = 1
    while counter <= n:
        eid = cookieConfig.eidConfig[name]
        thread = jdThread(i, "B-" + str(i) + ' ' + name, headers, eid)
        thread.start()
        threads.append(thread)
        i += 1
        counter += 1
    pass

# 等待所有线程完成
for t in threads:
    t.join()
print ("销毁原型机")