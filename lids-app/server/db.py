import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',

    database='lids-database',
    port=3306
)
cursor = db.cursor()
