import mysql.connector
import config.mysql as mysqlConfig
import time
import crawler.ziroomList as ziroomList
import threading
import queue

# 定义计数变量
exitFlag = 0
threadNum = 3

## 初始化爬虫线程
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("开启线程：" + self.name)
        threadRealRun(self.name, self.q)
        print ("退出线程：" + self.name)

def threadRealRun(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print ("%s 执行类型 %s" % (threadName, data))
            getListData(data)
        else:
            queueLock.release()
        time.sleep(1)

def getListData(data):
    # 分类爬取
    conn = mysql.connector.connect(**mysqlConfig.config)
    cursor = conn.cursor(dictionary=True)
    try:

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
    thread = myThread(i, 'thread-' + str(i), workQueue)
    thread.start()
    threads.append(thread)
    i += 1

# 填充队列
i = 1
queueLock.acquire()
workQueue.put(1)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")



