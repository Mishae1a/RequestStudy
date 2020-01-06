import mysql.connector
import config.mysql as mysqlConfig
import time
import crawler.LianjiaDetail as LianjiaDetail
import threading
from datetime import datetime
import redis

def dealData(cursor, conn, rds):
    detailObj = LianjiaDetail.LianjiaDetail()
    lj_id = rds.lpop('ljDetail')
    if (lj_id == None):
        return False
    # Read a single record
    sql = "select * from lj_transaction WHERE lj_id='" + str(lj_id, encoding = "utf-8") + "' LIMIT 1"
    cursor.execute(sql)
    ljList = cursor.fetchall()
    if len(ljList) == 0:
        return False
    for result in ljList:
        # result = cursor.fetchone()
        # 取详情数据
        url = "https://" + result['city_code'] + ".lianjia.com/chengjiao/" + result['lj_id'] + ".html"
        ljDetail = detailObj.getUrlData(result['lj_id'], url)
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

conn = mysql.connector.connect(**mysqlConfig.config)
cursor = conn.cursor(dictionary=True)
rds = redis.Redis(host='127.0.0.1', port=6379, password='ectouch')
while 1:
    r = dealData(cursor, conn, rds)
    if r == False:
        break