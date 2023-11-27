#
# @author Ricardo Sida, Carlos Alcazar and Denisse Fernandez
# @version 5.0, 11/26/23
#

from flask import request, jsonify
from db import cursor, db
from xml.etree import ElementTree as ET
import json

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
        cursor.execute("SELECT * FROM alert WHERE dest_ip = '127.0.0.1'")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[1], 'time': alert[2], 'source_ip': alert[3], 'dest_ip': alert[4], 'port': alert[5], 'desc': alert[7], 'protocol': alert[6], 'id': alert[0]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def get_alerts_level():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT * FROM alert WHERE dest_ip = '127.0.0.1' ORDER BY level ASC")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[1], 'time': alert[2], 'source_ip': alert[3], 'dest_ip': alert[4], 'port': alert[5], 'desc': alert[7], 'protocol': alert[6], 'id': alert[0]} for alert in alerts] #SRC/DEST PORT

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)

def get_alerts_time():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT * FROM alert WHERE dest_ip = '127.0.0.1' ORDER BY time ASC")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[1], 'time': alert[2], 'source_ip': alert[3], 'dest_ip': alert[4], 'port': alert[5], 'desc': alert[7], 'protocol': alert[6], 'id': alert[0]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def get_alerts_ip():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT * FROM alert WHERE dest_ip = '127.0.0.1' ORDER BY source_ip ASC")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[1], 'time': alert[2], 'source_ip': alert[3], 'dest_ip': alert[4], 'port': alert[5], 'desc': alert[7], 'protocol': alert[6], 'id': alert[0]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def get_alerts_protocol():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT * FROM alert WHERE dest_ip = '127.0.0.1' ORDER BY protocol ASC")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[1], 'time': alert[2], 'source_ip': alert[3], 'dest_ip': alert[4], 'port': alert[5], 'desc': alert[7], 'protocol': alert[6], 'id': alert[0]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def filter_level_1():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT * FROM alert WHERE dest_ip = '127.0.0.1' AND level = '1'")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[1], 'time': alert[2], 'source_ip': alert[3], 'dest_ip': alert[4], 'port': alert[5], 'desc': alert[7], 'protocol': alert[6], 'id': alert[0]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)

def filter_level_2():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT * FROM alert WHERE dest_ip = '127.0.0.1' AND level = '2'")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[1], 'time': alert[2], 'source_ip': alert[3], 'dest_ip': alert[4], 'port': alert[5], 'desc': alert[7], 'protocol': alert[6], 'id': alert[0]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def filter_level_3():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT * FROM alert WHERE dest_ip = '127.0.0.1' AND level = '3'")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[1], 'time': alert[2], 'source_ip': alert[3], 'dest_ip': alert[4], 'port': alert[5], 'desc': alert[7], 'protocol': alert[6], 'id': alert[0]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def post_alert_details():
    details = request.data.decode('utf-8')
    details_dict = json.loads(details)

    id = details_dict.get('id')
    desc = details_dict.get('desc')
    dest_ip = details_dict.get('dest_ip')
    level = details_dict.get('level')
    port = details_dict.get('port')
    protocol = details_dict.get('protocol')
    source_ip = details_dict.get('source_ip')
    time = details_dict.get('time')
    #src_port = details_dict.get('src_port')
    #dest_port = details_dict.get('dest_port')
    
    #return details_dict
    return jsonify(details_dict)

def get_alert_details():
    data = request.data
    return data