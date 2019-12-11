import pymysql.cursors

# Connect to the database
config = {
    'host':'127.0.0.1',
    'user':'ectouch',
    'password':'ecTouchZS123',
    'db':'ectouch',
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor
}
connection = pymysql.connect(**config)

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "select * from ecs_order_info WHERE order_id=%s LIMIT 1"
        cursor.execute(sql, (4162,))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()