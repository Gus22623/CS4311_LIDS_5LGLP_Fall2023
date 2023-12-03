#
# @author Ricardo Sida, Carlos Alcazar and Denisse Fernandez
# @version 5.0, 11/26/23
#

from flask import Flask
from flask_cors import CORS
import routes
from datetime import datetime
from LIDS_Agent import PacketCapture
from LIDS_Agent import open_pcap_file
from LIDS_Agent import config
from LIDS_Agent import Alerts
from db import cursor, db
import socket

'''THIS WILL BE MOVED TO ROUTES for the queries (also will be used in React - Carlos)'''
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("Your Computer Name is:"+hostname)
print("Your Computer IP Address is:"+IPAddr)

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/upload-xml', methods=['POST'])
def handle_upload():
    return routes.upload_xml()

@app.route('/getAlerts', methods=['GET'])
def get_alerts():
    return routes.getAlerts()

@app.route('/getAlertsLevel', methods=['GET'])
def get_alerts_level():
    return routes.get_alerts_level()

@app.route('/getAlertsTime', methods=['GET'])
def get_alerts_time():
    return routes.get_alerts_time()

@app.route('/getAlertsIP', methods=['GET'])
def get_alerts_ip():
    return routes.get_alerts_ip()

@app.route('/filterLevel_1', methods=['GET'])
def filter_level_1():
    return routes.filter_level_1()

@app.route('/filterLevel_2', methods=['GET'])
def filter_level_2():
    return routes.filter_level_2()

@app.route('/filterLevel_3', methods=['GET'])
def filter_level_3():
    return routes.filter_level_3()

@app.route('/alert-details', methods=['POST'])
def post_alert_details():
    return routes.post_alert_details()

@app.route('/alert-details', methods=['GET'])
def get_alert_details():
    return routes.get_alert_details()

if __name__ == '__main__':
    #app.run(debug=True, port=5000)

    # Create an instance of PacketCapture
    packet_capture = PacketCapture(interface="Wi-Fi")
    my_Config = config()

    # Flag to track if packet capture is active
    capturing = False 
    
    while(True):
        packet_capture.configuration = my_Config.configurations
        packet_capture.start_capture()

        alerts = Alerts()
        alerts_table = alerts.displayAlerts()
        #print(alerts_table)
        app.run(debug=True, port=5000)


