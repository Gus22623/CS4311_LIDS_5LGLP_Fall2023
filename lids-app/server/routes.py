from flask import request, jsonify
from db import cursor, db
from xml.etree import ElementTree as ET

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

def getAlerts():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT * FROM alert")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'alertID': alert[0], 'source_IP': alert[1], 'dest_IP': alert[2], 
                        'sourcePort': alert[3], 'destPort': alert[4], 'reason': alert[5], 
                        'severity': alert[6]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
