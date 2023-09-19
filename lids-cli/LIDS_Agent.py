import xml.etree.ElementTree as ET
import os, sys, re
from socket import socket, AF_INET, SOCK_STREAM, SOCK_RAW, IPPROTO_TCP
import threading
import time 

# Variables used in LIDS
#stigFile = {JSON file containing STIG rules}
configFile = None
#maliciousPackets = []
#alertList = []
#serverAddress = {IP address of server}
#serverPort = {Port of server}
#alert = {Alert String}

def test(int):
    return 1
def ingestConfig(configFile):
    try:
        # Load the XML configuration file
        tree = ET.parse(configFile)
        root = tree.getroot()

        # Process the XML data
        for system in root.findall('./system'):
            name = system.find('name').text
            ip = system.find('ip').text
            mac = system.find('mac').text
            ports = [int(port) for port in system.find('ports').text.split(',')]
            whitelist = system.find('whitelist').text.split(',')
            

            print(f"Agent Name: {name}")
            print(f"IP Address: {ip}")
            print(f"MAC Address: {mac}")
            print(f"Ports: {ports}")
            print(f"Whitelist: {whitelist}\n")

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
        
# def connectToServer():
#     #TODO: Implement server connection logic here
#     pass


# def analyze_packet(packet):
#     #TODO: Implement packet analysis logic here
#     # Check for unknown IPs, port scans, failed login attempts, abnormal traffic
#     pass
# def generate_alert(event_type, details, timeStamp):
#     alert = f"{event_type}: {details}: {timeStamp}"
#     pass
    
# def display_alert(alert):
#     #TODO: Implement alert display logic here
#     print(alert)
#     pass

# def encrypt_and_send_alert(alert):
#     #Encrypt the alert data
#     key = Fernet.generate_key()
#     cipher_suite = Fernet(key)
#     cipher_text = cipher_suite.encrypt(alert)
    
#     #Send the encrypted alert to LIDS-D agent
    
# def sniffTraffic():
#     #Start packet capture and analysis
#     while True:
#         sniff(filter="ip", prn=analyze_packet)
