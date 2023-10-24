import pymysql

db = pymysql.connect(
    host='127.0.0.1',
    user='root',

    database='lids-db',
    port=3001
)
cursor = db.cursor()