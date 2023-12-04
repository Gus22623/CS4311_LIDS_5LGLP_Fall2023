# LIDS_Agent back end code.

import os
import pyshark
import threading
import subprocess
from datetime import datetime
import xml.etree.ElementTree as ET
from collections import defaultdict
import asyncio
from pyshark import FileCapture
import csv

"""
NOTE: Wireshark needs to be installed in your machine to use pyshark
NOTE: Use 'pip install pyshark' to install pyshark
"""
class config:
    def __init__(self):
        self.configurations = {}  # Dictionary to store configurations

    def ingestConfig(self, configFile):
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
                
                # Add the configuration to the dictionary
                self.configurations[name] = {
                    'Name': name,
                    'IP Address': ip,
                    'MAC Address': mac,
                    'Ports': ports,
                    'Whitelist': whitelist
                }
                
                # Display the configuration
                print(f"Agent Name: {self.configurations[name]['Name']}")
                print(f"IP Address: {self.configurations[name]['IP Address']}")
                print(f"MAC Address: {self.configurations[name]['MAC Address']}")
                print(f"Ports: {self.configurations[name]['Ports']}")
                print(f"Whitelist: {self.configurations[name]['Whitelist']}\n")

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

# Class to handle packet capture
class PacketCapture:
    def __init__(self, interface='eth0'):
        self.interface = interface
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
 
                
    # Method to detect port scan
    def detect_port_scan(self, packet, connection_attempts, threshold=50):
        source_ip = packet.ip.src
        
        connection_attempts[source_ip] += 1

        if connection_attempts[source_ip] >= threshold:
            self.create_alert(packet, self.port_scan)
            
        
    # Method to create the alert and display it to the user
    def create_alert(self, packet, description):
        # Create an alert object to store alerts and its attributes
        alerts = Alert()
        alerts.source = packet.ip.src
        alerts.destination = packet.ip.dst
        alerts.protocol = packet.transport_layer
        alerts.length = packet.length
        alerts.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        alerts.description = description
        
        # Store the alert in the list
        self.alerts.append(alerts)
        
        # Specify the path to your CSV file
        csv_file_path = "/media/kali/ESD-USB/alerts.csv"

        # Write the alert to the an external drive
        with open(csv_file_path, mode='a', newline='') as csv_file:
            fieldnames = ['Time', 'Source', 'Destination', 'Protocol', 'Length', 'Description']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Check if the CSV file is empty, write header if it is
            if csv_file.tell() == 0:
                writer.writeheader()

            # Write the alert data to the CSV file
            writer.writerow({
                'Time': alerts.time,
                'Source': alerts.source,
                'Destination': alerts.destination,
                'Protocol': alerts.protocol,
                'Length': alerts.length,
                'Description': alerts.description
            })
        
        # Display the alert to the user
        print(f"Time: {alerts.time}, Source: {alerts.source}, Destination: {alerts.destination}, Protocol: {alerts.protocol}, Length: {alerts.length}, Description: {alerts.description}")

# Class to store alerts and its attributes
class Alert:
    def __init__(self):
        self.source = None
        self.destination = None
        self.protocol = None
        self.length = None
        self.description = None
        self.time = None


            