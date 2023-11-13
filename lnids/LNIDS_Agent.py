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
        
def connectToServer():
    # TODO: Implement connection logic here
    pass


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

            #-----------------------------------For Debugging-------------------------------------------------#
            # Packet information
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            
            # if 'IP' in packet:
            #     src = packet.ip.src
            #     dst = packet.ip.dst

            #     if 'TCP' in packet:
            #         protocol = 'TCP'
            #         packet_length = int(packet.length)
            #         flags = packet.tcp.flags

            #         if 'SYN' in flags:
            #             description = 'TCP Handshake SYN'
            #         else:
            #             description = 'Other TCP Packet'
            #     elif 'UDP' in packet:
            #         protocol = 'UDP'
            #         packet_length = int(packet.length)
            #         description = 'UDP Packet'
            #     elif 'ICMP' in packet:
            #         protocol = 'ICMP'
            #         packet_length = int(packet.length)
            #         description = 'ICMP Packet'
            #     elif 'ARP' in packet:
            #         protocol = 'ARP'
            #         packet_length = int(packet.length)
            #         description = 'ARP Packet'
            #     elif 'HTTP' in packet:
            #         protocol = 'HTTP'
            #         packet_length = int(packet.length)
            #         description = 'HTTP Packet'
            #     else:
            #         protocol = 'Other'
            #         packet_length = int(packet.length)
            #         description = "Unknown/Other Protocol"
            
            # """
            # NOTE:Displaying packet information for debugging purposes
            # Uncomment the following line to display packet information
            # | |
            # V V
            # """
            # print(f"Time: {time}, Source: {src}, Destination: {dst}, Protocol: {protocol}, Length: {packet_length}, Description: {description}")
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
        # TODO: Implement failed login attempt logic here
        pass
        
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
        
        # Specify the path on your external drive where you want to save alerts
        # external_drive_path = "/media/kali/8874-BD0E/"
        # alerts_file_path = os.path.join(external_drive_path, "alerts.txt")
        
        # TODO: Save the alerts to a pcap file in an external drive
        # Specify the path to your CSV file
        csv_file_path = "/media/kali/8874-BD0E/alerts.csv"

        # Write the alert to the CSV file
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


            