import mysql.connector


config = {
    'host': '127.0.0.1',
    'user': 'ectouch',
    'password': 'ecTouchZS123',
    'port': 3306,
    'database': 'ectouch',
    'charset': 'utf8',
    # 'cursor_class' : mysql.connector.cursor.MySQLCursorDict,
}
conn = mysql.connector.connect(**config)
cursor = conn.cursor(dictionary=True)

cursor.execute('select * from ecs_order_info LIMIT 1')
values = cursor.fetchone()
print(values['goods_amount'])

