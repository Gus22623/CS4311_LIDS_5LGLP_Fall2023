import xml.etree.ElementTree as ET
from socket import socket, AF_INET, SOCK_STREAM, SOCK_RAW, IPPROTO_TCP
import threading
from datetime import datetime
import pyshark

"""
NOTE: Use pip install pyshark to install pyshark
Used to capture packets
"""

# Variables used in LIDS
#stigFile = {JSON file containing STIG rules}
configFile = None
#maliciousPackets = []
#alertList = []
#serverAddress = {IP address of server}
#serverPort = {Port of server}
#alert = {Alert String}
Names = []
IPs = []
whiteList = []
MACList = []


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
            
            # append information to lists
            

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
    
# def sniffTraffic(capture):
#     #Start packet capture and analysis

# class PacketCapture:
#     def __init__(self, interface='Wi-Fi', display_filter='tcp'):
#         self.interface = interface
#         self.display_filter = display_filter
#         self.capture = pyshark.LiveCapture(interface=interface)
#         self.capture_thread = None

#     def start_capture(self):
#         if self.capture_thread is None or not self.capture_thread.is_alive():
#             print("Packet capture started. Type 'quit' to stop.")
#             self.capture_thread = threading.Thread(target=self._capture_packets)
#             self.capture_thread.start()

#     def stop_capture(self):
#         if self.capture_thread and self.capture_thread.is_alive():
#             self.capture_thread.join()
#             print("Packet capture stopped.")

#     def _capture_packets(self):
#         # Start capturing packets
#         for packet in self.capture.sniff_continuously(packet_count=0):
#             continue
            
#     def display_packets(self):
#         # Display packets captured
#         for packet in self.capture:
#             print(packet)
