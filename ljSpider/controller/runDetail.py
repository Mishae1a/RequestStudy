import mysql.connector
import config.mysql as mysqlConfig
import time
import crawler.LianjiaDetail as LianjiaDetail
import threading
from datetime import datetime

# 定义计数变量
exitFlag = 0
threadNum = 10
hasInsert = False

## 初始化爬虫线程
class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("生成线程：" + self.name)
        conn = mysql.connector.connect(**mysqlConfig.config)
        cursor = conn.cursor(dictionary=True)
        while 1:
            r = dealData(cursor, conn)
            if r == False:
                break
        print ("销毁线程：" + self.name)

def dealData(cursor, conn):
    detailObj = LianjiaDetail.LianjiaDetail()
    # Read a single record
    sql = "select * from lj_transaction WHERE status=1 ORDER BY rand() LIMIT 20"
    cursor.execute(sql)
    ljList = cursor.fetchall()
    if len(ljList) == 0:
        return False
    for result in ljList:
        # result = cursor.fetchone()
        # 取详情数据
        ljDetail = detailObj.getUrlData(result['lj_id'])
        if (ljDetail == False):
            print(result['lj_id'] + ' 获取详情数据失败！')
            return False
        # 更新详情数据
        cursor.execute("UPDATE lj_transaction SET floor = %(floor)s, house_type = %(house_type)s, area = %(area)s," 
            + " real_araa = %(real_araa)s, guapai_time = %(guapai_time)s, ownership = %(ownership)s, house_usage = %(house_usage)s,"
            + " house_limit = %(house_limit)s, attr_detail = %(attr_detail)s, trade_list = %(trade_list)s, plot = %(plot)s, "
            + " plot_id = %(plot_id)s, location = %(location)s, status=2 WHERE lj_id=%(lj_id)s", ljDetail)
        conn.commit()
    return True
    # pass

## 从列表开始 获取队列
threads = []

# 创建新线程
i = 1
while i <= threadNum:
    thread = myThread(i, 'B-' + str(i))
    thread.start()
    threads.append(thread)
    i += 1
    time.sleep(1)

# 等待所有线程完成
for t in threads:
    t.join()
print ("销毁主线程")

# now = datetime.now()
# signTime = now.strftime(r"%m%d%H")
# print ("%s 扫描结果：%s" % (signTime, hasInsert))
# if (hasInsert):
#     smsObj = Sms.Sms()
#     smsObj.sendMsg(smsConfig.config['mobile'], '时间：' + signTime + '，有新提醒')

