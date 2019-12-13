import mysql.connector
import config.mysql as mysqlConfig
import time
import crawler.LianjiaDetail as LianjiaDetail
import threading
from datetime import datetime
import redis




# 定义计数变量
exitFlag = 0
threadNum = 1
hasInsert = False

def dealData():
    r = redis.Redis(host='127.0.0.1', port=6379, password='ectouch')
    conn = mysql.connector.connect(**mysqlConfig.config)
    cursor = conn.cursor(dictionary=True)
    # detailObj = LianjiaDetail.LianjiaDetail()
    # Read a single record
    sql = "select lj_id from lj_transaction WHERE status=1 LIMIT 1000000"
    cursor.execute(sql)
    ljList = cursor.fetchall()
    for item in ljList:
        r.lpush('ljDetail', str(item['lj_id']))
    print(r.llen('ljDetail'))

dealData()
