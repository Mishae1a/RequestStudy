import mysql.connector
import config.mysql as mysqlConfig
import crawler.ZiroomList as ZiroomList
import queue

def getListData(data):
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
                
                # 有3000以下的新房子 发送短信通知
                if (float(house['price']) < 3000):
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


getListData('三丰里')



