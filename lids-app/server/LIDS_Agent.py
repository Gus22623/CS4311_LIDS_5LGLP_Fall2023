###########################################################
# @author Ricardo Sida and Gustavo Ramirez
# @author Carlos Alcazar and Denisse Fernandez
# @version 0.2
###########################################################
###########################################################
# Modification
# @author Alejandro Jaramillo & Ruth Avila
# @version 0.2
# @description: Add Alert Encryption functionality.
###########################################################

# LIDS_Agent back end code.

from http.client import HTTPResponse
import os
import pyshark
import threading
import subprocess
from datetime import datetime
import xml.etree.ElementTree as ET
from db import cursor, db
from prettytable import PrettyTable
from collections import defaultdict
import asyncio
from cryptography.fernet import Fernet
import socket
from socket import AF_INET, SOCK_STREAM
import base64
import time

"""
NOTE: Wireshark needs to be installed in your machine to use pyshark
NOTE: Use 'pip install pyshark' to install pyshark
"""
class config:
    def __init__(self):
        self.configurations = {}  # Dictionary to store configurations

    def ingestConfig(self, configFile):
        try:
            # Parse the XML data
            root = ET.fromstring(configFile)
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
            return True

        except ET.ParseError:
            print("Error: Invalid XML file format.")
            return
        except FileNotFoundError:
            print("Error: File not found.")
            return
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return
        
def connectToServer():
    # TODO: Implement connection logic here
    pass

class Connection():
    def __init__(self):
        self.connection = None
        self.address = None
        self.port = None
        self.serverSocket = None

    def connect_to_server(self, server_address, server_port):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((server_address, server_port))
            self.address, self.port = self.connection.getsockname()
            print(f"Connected to {server_address} on port {server_port}")

        except Exception as e:
            print(f"Error connecting to server: {str(e)}")
    
    def send_alert(self, alert_data):
        try:
            #key = b'LidsTeam5Key1234567890123456'[:32]
            key = b'u-Tab2rqhRSPz5IO4yz_qy3fGtAQr-ohHahuPXSsidg='
            #key = base64.urlsafe_b64encode(key)
            cipher_suite = Fernet(key)

            if self.connection:
                alert_str = f"{alert_data['level']},{alert_data['time']},{alert_data['source_ip']},{alert_data['dest_ip']},{alert_data['source_port']},{alert_data['dest_port']},{alert_data['protocol']},{alert_data['description']}"
                alert_str = alert_str.encode()
                encrypted_data = cipher_suite.encrypt(alert_str)

                self.connection.sendall(encrypted_data)
            else:
                print("Error: Not connected to server")
        except Exception as e:
            print(f"Error sending alert to server: {str(e)}")


# Method to display saved PCAP file in Wireshark
def open_pcap_file(pcap_file_path):
    try:
        """
        NOTE: Wireshark needs to be in your system's PATH environment variable, or you can specify the path to the Wireshark executable below
              You may need to restart your machine after installing Wireshark for the PATH variable to be updated
        NOTE: Use yourPcapFile.pcapng format for the PCAP file
        """
        # List of common Wireshark executable names on different platforms
        possible_executables = ["wireshark","Wireshark.exe"]


        # Iterate through each directory in the PATH environment variable
        for directory in os.environ["PATH"].split(os.pathsep):
            for executable in possible_executables:
                executable_path = os.path.join(directory, executable)
                if os.path.isfile(executable_path):
                    wireSharkPath = executable_path
                    print(f"Found Wireshark executable at: {wireSharkPath}")
                    print(f"Opening PCAP file: {pcap_file_path}")
                    # Launch Wireshark with the provided PCAP file path
                    
                    """NOTE: Placeholder in case the above implementation does not work. Change the path to the Wireshark executable on your machine"""          
                    # wireSharkPath = "C:\Program Files\Wireshark\Wireshark.exe" # ""<- Placeholder path""
                    subprocess.Popen([wireSharkPath, pcap_file_path])
                    
    except FileNotFoundError:
        print("Wireshark is not installed or not in your system's PATH.")
    except Exception as e:
        print(f"Error opening PCAP file: {str(e)}")

# Class to handle packet capture
class PacketCapture:
    def __init__(self, interface='Wi-Fi', server_address='127.0.0.1', server_port=5010):
        self.interface = interface
        # self.display_filter = display_filter - NOTE: Removed this filter to capture all packets
        self.capture = pyshark.LiveCapture(interface=interface)
        self.capture_thread = None
        self.is_capturing = False
        self._display_packets = False
        self.restart_timer = None  # Timer for thread restart
        self.configuration = None  # Configuration dictionary passed from the configuration class
        self.alerts = []  # List to store alerts
        
        # Blacklist
        self.blacklist = []
        
        # Thread to start replaying a PCAP file
        self.replay_thread = None
        self.is_replaying = False
        
        # Dictionary to store connection attempts
        self.connection_attempts = defaultdict(int)
        
        # Types of alert descriptions
        self.unknown_IP = "Unknown IP Address"
        self.port_scan = "Port Scan"
        self.failed_login = "Failed Login Attempt"

        #Connection object and variables to LIDS-D
        self.server_address = server_address
        self.server_port = server_port
        self.connection = Connection()
        self.connection.connect_to_server(self.server_address, self.server_port)

    # Method to start packet capture
    def start_capture(self):
        if not self.is_capturing:
            print("Packet capture started in the background.")
            self.is_capturing = True
            self.capture_thread = threading.Thread(target=self._capture_packets)
            self.capture_thread.start()
            self.restart_timer = threading.Timer(120.0, self.restart_capture_thread)
            self.restart_timer.daemon = True
            self.restart_timer.start()  # Start the timer

    # Method to stop packet capture
    def stop_capture(self):
        if self.is_capturing:
            self.is_capturing = False
            self.capture_thread.join()
            print("Packet capture stopped.")

    # Restart the packet capture thread every 2 minutes
    def restart_capture_thread(self):
        if self.is_capturing:
            self.is_capturing = False  # Stop the current capture thread
            self.capture_thread.join()
            print("Restarting packet capture thread after 2 minutes.")
            self.is_capturing = True
            self.capture_thread = threading.Thread(target=self._capture_packets)
            self.capture_thread.start()
            self.restart_timer = threading.Timer(120.0, self.restart_capture_thread)
            self.restart_timer.daemon = True
            self.restart_timer.start()  # Start the timer
        
    # Method to capture packets
    def _capture_packets(self):
        for packet in self.capture.sniff_continuously(packet_count=0):
            if not self.is_capturing:
                break   

            #-----------------------------------For Debugging-------------------------------------------------#
            # # Packet information
            # time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            # if 'IP' in packet:
            #     src = packet.ip.src
            #     dst = packet.ip.dst

                if 'TCP' in packet:
                    protocol = 'TCP'
                    packet_length = int(packet.length)
                    flags = packet.tcp.flags
                    src_port = packet.tcp.srcport
                    dest_port = packet.tcp.dstport

                    if 'SYN' in flags:
                        description = 'TCP Handshake SYN'
                    else:
                        description = 'Other TCP Packet'
                elif 'UDP' in packet:
                    protocol = 'UDP'
                    packet_length = int(packet.length)
                    description = 'UDP Packet'
                    src_port = packet.udp.srcport
                    dest_port = packet.udp.dstport
                elif 'ICMP' in packet:
                    protocol = 'ICMP'
                    packet_length = int(packet.length)
                    description = 'ICMP Packet'
                    src_port = ''
                    dest_port = ''
                elif 'ARP' in packet:
                    protocol = 'ARP'
                    packet_length = int(packet.length)
                    description = 'ARP Packet'
                    src_port = ''
                    dest_port = ''
                elif 'HTTP' in packet:
                    protocol = 'HTTP'
                    packet_length = int(packet.length)
                    description = 'HTTP Packet'
                    src_port = packet.tcp.srcport
                    dest_port = packet.tcp.dstport
                else:
                    protocol = 'Other'
                    packet_length = int(packet.length)
                    description = "Unknown/Other Protocol"
                    src_port = ''
                    dest_port = ''
                
                """
                NOTE:Displaying packet information for debugging purposes
                Uncomment the following line to display packet information
                | |
                V V
                """
                # Create a dictionary to represent the packet
                packet_info = {
                    'Time': time,
                    'Source': src,
                    'Destination': dst,
                    'Protocol': protocol,
                    'Length': packet_length,
                    'Description': description,
                    'Src Port': src_port,
                    'Dest Port': dest_port
                }

                print(f"Time: {time}, Source: {src}, Destination: {dst}, Protocol: {protocol}, Length: {packet_length}, Description: {description}, Src Port: {src_port}, Dest Port: {dest_port}")
            #------------------------------------------------------------------------------------#
            
            # TODO: Implement packet analysis logic here

            if 'IP' in packet:
                src = packet.ip.src
                dst = packet.ip.dst
                
                # Check if the source and destination IP addresses are in the configuration dictionary
                if src not in self.configuration:
                    self.create_alert(packet, self.unknown_IP)
                    
                if dst not in self.configuration:
                    self.create_alert(packet, self.unknown_IP)
                
                # Check for potential port scan
                self.detect_port_scan(packet, self.connection_attempts)
                
                # if 'TCP' in packet:
                #     protocol = 'TCP'
                #     packet_length = int(packet.length)
                #     flags = packet.tcp.flags

                #     if 'SYN' in flags:
                #         description = 'TCP Handshake SYN'
                #         if self.is_port_scan(packet, src):
                #             self.detect_alert(packet, f"Port scan detected from {src}")
                #     else:
                #         description = 'Other TCP Packet'
                
    # Method to detect port scan
    def detect_port_scan(self, packet, connection_attempts, threshold=50):
        source_ip = packet.ip.src
        
        connection_attempts[source_ip] += 1

        if connection_attempts[source_ip] >= threshold:
            self.create_alert(packet, self.port_scan)
            
    def failed_login_attempt(self, packet):
        if packet.haslayer(HTTPResponse):
            http_layer = packet.getlayer(HTTPResponse)
            if http_layer.Status_Code == 401:
                self.create_alert(packet, self.failed_login)
        
    # Method to create the alert and display it to the user
    def create_alert(self, packet, description):
        try:
            # Create an Alert object
            alert = Alert()
            alert.source = packet.ip.src
            print(alert.source)
            alert.destination = packet.ip.dst
            print(alert.destination)
            alert.protocol = packet.transport_layer
            alert.length = packet.length
            
            if 'TCP' in packet:
                alert.src_port = packet.tcp.srcport
                alert.dest_port = packet.tcp.dstport

            elif 'UDP' in packet:
                alert.src_port = packet.udp.srcport
                alert.dest_port = packet.udp.dstport

            elif 'ICMP' in packet:
                alert.src_port = ''
                alert.dest_port = ''
            else:
                alert.src_port = ''
                alert.dest_port = ''

            alert.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            alert.description = description
            #print("WHEREE", alert.level, alert.time, alert.source, alert.destination, alert.src_port, alert.dest_port, alert.protocol, alert.description)

            # Set the alert level based on the description
            if alert.description == self.unknown_IP:
                alert_level = 3
            elif alert.description == self.port_scan:
                alert_level = 2
            elif alert.description == self.failed_login:
                alert_level = 1
            else:
                alert_level = 0  # Set a default level if description doesn't match expected values

            alert_d = {
                "level": alert_level,
                "time": alert.time,
                "source_ip": alert.source,
                "dest_ip": alert.destination,
                "source_port": alert.src_port,
                "dest_port" : alert.dest_port,
                "protocol": alert.protocol,
                "description": alert.description
            }
            time.sleep(1)
            self.connection.send_alert(alert_d)

            '''
            # Execute SQL query to insert the alert data into the 'alert' table
            sql_insert_alert = (
                "INSERT INTO alert (level, time, source_ip, dest_ip, src_port, dest_port, protocol, description) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )

            cursor.execute(sql_insert_alert, (
                alert_level,
                alert.time,
                alert.source,
                alert.destination,
                alert.src_port, #alert.length
                alert.dest_port,
                alert.protocol,
                alert.description
            ))

            db.commit()
            '''
            #print("Alert stored in the database.")
        except Exception as e:
            print(f"Error storing alert in the database: {str(e)}")

# Class to store alerts and its attributes
class Alert:
    def __init__(self):
        self.source = None
        self.destination = None
        self.protocol = None
        #self.length = None
        self.src_port = None
        self.dest_port = None
        self.description = None
        self.time = None


class Alerts:
    def __init__(self):
        self.cursor = cursor

    def getAlerts(self):
        try:
            # Fetch data from the 'alerts' table
            self.cursor.execute("SELECT level, time, source_ip, port, description FROM alert")
            alerts = self.cursor.fetchall()

            # Convert data to a list of dictionaries for JSON response
            alerts_data = [{'level': alert[0], 'time': alert[1], 'source_ip': alert[2], 'port': alert[3], 'desc': alert[4]} for alert in alerts]

            return alerts_data
        except Exception as e:
            return str(e)

    def displayAlerts(self):
        alerts = self.getAlerts()

        if isinstance(alerts, list):
            # Create a pretty table
            table = PrettyTable()
            table.field_names = ["Level", "Time", "Source IP", "Port", "Description"]

            for alert in alerts:
                table.add_row([alert['level'], alert['time'], alert['source_ip'], alert['port'], alert['desc']])

            return str(table)
        else:
            return f"Error: {alerts}"