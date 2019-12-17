import mysql.connector
import config.mysql as mysqlConfig
import time
import crawler.ZjwBeijing as ZjwBeijing

zjwObj = ZjwBeijing.ZjwBeijing()
result = zjwObj.getUrlData()

conn = mysql.connector.connect(**mysqlConfig.config)
cursor = conn.cursor(dictionary=True)
cursor.execute("INSERT INTO zjw_beijing (dt, net_number, net_area, residence_number, residence_area) "
    + " VALUES (%(dt)s, %(net_number)s, %(net_area)s, %(residence_number)s, %(residence_area)s)",
    result
)
conn.commit()
