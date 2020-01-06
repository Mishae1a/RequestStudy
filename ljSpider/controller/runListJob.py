import crawler.LianjiaList as LianjiaList
import config.pageConf as pageConf
import mysql.connector
import config.mysql as mysqlConfig
import time
import redis
import re

# 获取一个实际分片后的url的数据
def getListData(page):
    # 分类爬取
    conn = mysql.connector.connect(**mysqlConfig.config)
    cursor = conn.cursor(dictionary=True)
    # 从page中重新截出来cityCode  //cq.lianjia.com
    cityCode = re.findall(r"//(.*).lianjia.com", page)
    cityCode = cityCode[0]
    pg = 1
    while 1:
        # try:
        lianjiaObj = LianjiaList.LianjiaList()
        houseList = lianjiaObj.getUrlData(page + 'pg' + str(pg))
        # print(page + 'pg' + str(pg))
        if (houseList['code'] != 0):
            print(page + ' 页面请求失败' + str(houseList['code']) + houseList['msg'])
            return
        for house in houseList['data']:
            # Read a single record
            sql = "select * from lj_transaction WHERE lj_id = %s LIMIT 1"
            print(house)
            house['city_code'] = cityCode
            cursor.execute(sql, (house['lj_id'],))
            result = cursor.fetchone()
            if (result == None):
                cursor.execute("INSERT INTO lj_transaction (lj_id, city_code, title, trade_time, total_price, total_unit, unit_price, unit_unit, status) "
                        + " VALUES (%(lj_id)s, %(city_code)s, %(title)s, %(trade_time)s, %(total_price)s, %(total_unit)s, %(unit_price)s, %(unit_unit)s, %(status)s)",
                        house
                    )
                conn.commit()
            else:
                # 更新原有的
                # cursor.execute("UPDATE lj_transaction SET title = %(title)s, trade_time = %(trade_time)s, total_price = %(total_price)s," 
                #     +" total_unit = %(total_unit)s, unit_price = %(unit_price)s, unit_unit = %(unit_unit)s, status = %(status)s, keyword = %(keyword)s WHERE lj_id=%(lj_id)s", house)
                # conn.commit()
                # 列表页似乎也不用更新
                pass
        # 如果本页数据不为空 继续抓下一页
        if (len(houseList['data']) == 0):
            break
        else:
            pg += 1
        if (pg >= 100):
            break
        # except BaseException as e:
        #     print('[error] [%s] [%s]' % (page, e))

    cursor.close()
    conn.close()
    pass


def run():
    rds = redis.Redis(host='127.0.0.1', port=6379, password='ectouch')
    while(1):
        listJob = rds.lpop('spider:ljList')
        if (listJob == None):
            return False
        jobPage = str(listJob, encoding = "utf-8")
        getListData(jobPage)
    
    
