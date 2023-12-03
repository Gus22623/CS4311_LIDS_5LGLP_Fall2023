import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    password='pass123',

    database='lids-db',
    port=3306
)
cursor = db.cursor()
