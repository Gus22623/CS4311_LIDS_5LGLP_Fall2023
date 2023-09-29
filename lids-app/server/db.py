import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    database='lids-db',
    port=3001
)
cursor = db.cursor()
