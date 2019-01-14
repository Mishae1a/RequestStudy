import mysql.connector
import config.mysql as mysqlConfig
import time
import crawler.ZiroomList as ZiroomList
import threading
import queue
import spiderUnit.Sms as Sms
import config.sms as smsConfig
from datetime import datetime

# 定义计数变量
exitFlag = 0
threadNum = 3
hasInsert = False

## 初始化爬虫线程
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("生成机体：" + self.name)
        threadRealRun(self.name, self.q)
        print ("销毁机体：" + self.name)

def threadRealRun(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print ("%s 扫描地区 %s" % (threadName, data))
            getListData(data)
        else:
            queueLock.release()
        time.sleep(1)

def getListData(data):
    global hasInsert
    # 分类爬取
    conn = mysql.connector.connect(**mysqlConfig.config)
    cursor = conn.cursor(dictionary=True)
    try:
        ziroomListObj = ZiroomList.ZiroomList(data)
        houseList = ziroomListObj.getDataList()
        for house in houseList:
            house['keyword'] = data
            # Read a single record
            sql = "select * from ziroom_price WHERE zid = %s LIMIT 1"
            cursor.execute(sql, (house['zid'],))
            result = cursor.fetchone()
            # exit()
            if (result == None):
                cursor.execute("INSERT INTO ziroom_price (zid, price, house_name, detail, area, floor, tags, unit, keyword) "
                        + " VALUES (%(zid)s, %(price)s, %(house_name)s, %(detail)s, %(area)s, %(floor)s, %(tags)s, %(unit)s, %(keyword)s)",
                        house
                    )
                conn.commit()
                
                # 有2600以下的新房子 发送短信通知
                if (float(house['price']) < 2600 && house['unit'] == '(每月)'):
                    hasInsert = True
            else:
                # 更新原有的
                cursor.execute("UPDATE ziroom_price SET price = %(price)s, house_name = %(house_name)s, detail = %(detail)s," 
                    +" area = %(area)s, floor = %(floor)s, tags = %(tags)s, unit = %(unit)s, keyword = %(keyword)s WHERE zid=%(zid)s", house)
                conn.commit()
    except BaseException as e:
        print('[error] [%s] [%s]' % (data, e))

    cursor.close()
    conn.close()
    pass

## 从列表开始 获取队列
queueLock = threading.Lock()
workQueue = queue.Queue(500)
threads = []

# 创建新线程
i = 1
while i <= threadNum:
    thread = myThread(i, 'B-' + str(i), workQueue)
    thread.start()
    threads.append(thread)
    i += 1

# 填充队列
i = 1
keywordList = [
    '三丰里',
    '天福园',
    '芳草地西街',
    '芳草地',
    '雅宝里',
    '芳草苑',
    '日坛北路',
    '吉祥里',
    '东大桥路',
    '东大桥东里',
    '向军南里',
    '关东店北街',
    '东草园',
    '西草园',
    '吉庆里',
    '怡景园',
    '建国里',
    '朝外市场街',
    '工人体育场',
    '日坛',
    '农丰里',
    '光华里',
]
queueLock.acquire()
for keyword in keywordList:
    workQueue.put(keyword)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("销毁原型机")

now = datetime.now()
signTime = now.strftime(r"%m%d%H")
print ("%s 扫描结果：%s" % (signTime, hasInsert))
if (hasInsert):
    smsObj = Sms.Sms()
    smsObj.sendMsg(smsConfig.config['mobile'], '时间：' + signTime + '，有新提醒')

