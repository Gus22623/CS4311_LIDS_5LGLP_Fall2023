import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',

    database='lids-db',
    port=3306
)
cursor = db.cursor()
