from flask import Flask, request
from flask_cors import CORS
import pymysql
from xml.etree import ElementTree as ET

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS for all routes

# Database Configuration
db = pymysql.connect(
    host='localhost',
    user='root', 
    database='lids-db',  # Replace with your database name
    port= 3001
)
cursor = db.cursor()

@app.route('/upload-xml', methods=['POST'])
def upload_xml():
    uploaded_file = request.data  # Get the raw data of the request

    # Parse the XML data
    root = ET.fromstring(uploaded_file)
    for system in root.findall('system'):
        name = system.find('name').text
        ip = system.find('ip').text
        mac = system.find('mac').text
        ports = system.find('ports').text
        whitelist = system.find('whitelist').text

       # Check if MAC address already exists in the database
        sql_check_mac = f"SELECT * FROM config WHERE mac = '{mac}'"
        cursor.execute(sql_check_mac)
        result = cursor.fetchone()

        if not result:
            # Insert data into MySQL database
            sql_insert = f"INSERT INTO config (name, ip, mac, ports, whitelist) VALUES ('{name}', '{ip}', '{mac}', '{ports}', '{whitelist}')"
            cursor.execute(sql_insert)
            db.commit()

    return "XML data successfully uploaded to MySQL"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
