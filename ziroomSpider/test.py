import mysql.connector
import config.mysql as mysqlConfig
import crawler.ZiroomList as ZiroomList
import queue

def getListData(data):
    # 分类爬取
    conn = mysql.connector.connect(**mysqlConfig.config)
    cursor = conn.cursor(dictionary=True)
    try:
        ziroomList = ZiroomList.ZiroomList(data)
        result = ziroomList.getDataList()
        print(result)
    except BaseException as e:
        print('[error] [%s] [%s]' % (data, e))

    cursor.close()
    conn.close()
    pass


getListData('三丰里')



