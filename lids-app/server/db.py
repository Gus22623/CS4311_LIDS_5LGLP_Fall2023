import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',

    database='lids-app',
    port=3301
)
cursor = db.cursor()
