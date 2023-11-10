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
        cursor.execute("SELECT level, time, source_ip, dest_ip, port, protocol, description FROM alert WHERE dest_ip = '127.0.0.1'")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[0], 'time': alert[1], 'source_ip': alert[2], 'dest_ip': alert[3], 'port': alert[4], 'protocol': alert[5], 'desc': alert[6]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def get_alerts_level():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT level, time, source_ip, dest_ip, port, protocol, description FROM alert WHERE dest_ip = '127.0.0.1' ORDER BY level ASC")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[0], 'time': alert[1], 'source_ip': alert[2], 'dest_ip': alert[3], 'port': alert[4], 'protocol': alert[5], 'desc': alert[6]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)

def get_alerts_time():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT level, time, source_ip, dest_ip, port, protocol, description FROM alert WHERE dest_ip = '127.0.0.1' ORDER BY time ASC")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[0], 'time': alert[1], 'source_ip': alert[2], 'dest_ip': alert[3], 'port': alert[4], 'protocol': alert[5], 'desc': alert[6]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def get_alerts_ip():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT level, time, source_ip, dest_ip, port, protocol, description FROM alert WHERE dest_ip = '127.0.0.1' ORDER BY source_ip ASC")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[0], 'time': alert[1], 'source_ip': alert[2], 'dest_ip': alert[3], 'port': alert[4], 'protocol': alert[5], 'desc': alert[6]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def get_alerts_protocol():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT level, time, source_ip, dest_ip, port, protocol, description FROM alert WHERE dest_ip = '127.0.0.1' ORDER BY protocol ASC")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[0], 'time': alert[1], 'source_ip': alert[2], 'dest_ip': alert[3], 'port': alert[4], 'protocol': alert[5], 'desc': alert[6]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def filter_level_1():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT level, time, source_ip, dest_ip, port, protocol, description FROM alert WHERE dest_ip = '127.0.0.1' AND level = '1'")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[0], 'time': alert[1], 'source_ip': alert[2], 'dest_ip': alert[3], 'port': alert[4], 'protocol': alert[5], 'desc': alert[6]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)

def filter_level_2():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT level, time, source_ip, dest_ip, port, protocol, description FROM alert WHERE dest_ip = '127.0.0.1' AND level = '2'")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[0], 'time': alert[1], 'source_ip': alert[2], 'dest_ip': alert[3], 'port': alert[4], 'protocol': alert[5], 'desc': alert[6]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)
    
def filter_level_3():
    try:
        # Fetch data from the 'alerts' table
        cursor.execute("SELECT level, time, source_ip, dest_ip, port, protocol, description FROM alert WHERE dest_ip = '127.0.0.1' AND level = '3'")
        alerts = cursor.fetchall()

         # Convert data to a list of dictionaries for JSON response
        alerts_data = [{'level': alert[0], 'time': alert[1], 'source_ip': alert[2], 'dest_ip': alert[3], 'port': alert[4], 'protocol': alert[5], 'desc': alert[6]} for alert in alerts]

        return jsonify(alerts_data)
    except Exception as e:
        return str(e)