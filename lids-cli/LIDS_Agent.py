# LIDS_Agent back end code.

import os
import pyshark
import threading
import subprocess
from datetime import datetime
import xml.etree.ElementTree as ET
from socket import socket, AF_INET, SOCK_STREAM

"""
NOTE: Use pip install pyshark to install pyshark
Wireshark needs to be installed in your machine to use pyshark
"""

configurations = {}  # Dictionary to store configurations

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
            
            # Add the configuration to the dictionary
            configurations[name] = {
                'Name': name,
                'IP Address': ip,
                'MAC Address': mac,
                'Ports': ports,
                'Whitelist': whitelist
            }
            
            # Display the configuration
            print(f"Agent Name: {configurations[name]['Name']}")
            print(f"IP Address: {configurations[name]['IP Address']}")
            print(f"MAC Address: {configurations[name]['MAC Address']}")
            print(f"Ports: {configurations[name]['Ports']}")
            print(f"Whitelist: {configurations[name]['Whitelist']}\n")

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
    #TODO: Implement server connection logic here
    pass

# Method to display saved PCAP file in Wireshark
def open_pcap_file(pcap_file_path):
    try:
        """
        NOTE: This code is not needed for the current implementation of the LIDS Agent
        Debugging code to find the Wireshark executable path
        Use yourPCAPFile.pcapng format for the PCAP file
        """
        # List of common Wireshark executable names on different platforms
        # possible_executables = ["Wireshark.exe"]


        # # Iterate through each directory in the PATH environment variable
        # for directory in os.environ["PATH"].split(os.pathsep):
        #     print(directory)
        #     for executable in possible_executables:
        #         executable_path = os.path.join(directory, executable)
        #         if os.path.isfile(executable_path):
        #             wireSharkPath = executable_path
        #             print(f"Found Wireshark executable at: {wireSharkPath}")
        #             print(f"Opening PCAP file: {pcap_file_path}")
        #             # Launch Wireshark with the provided PCAP file path
                    
        """NOTE: Change the path to the Wireshark executable on your machine"""          
        wireSharkPath = "C:\Program Files\Wireshark\Wireshark.exe"
        subprocess.run([wireSharkPath, pcap_file_path])
                    
    except FileNotFoundError:
        print("Wireshark is not installed or not in your system's PATH.")
    except Exception as e:
        print(f"Error opening PCAP file: {str(e)}")

# Class to handle packet capture
class PacketCapture:
    def __init__(self, interface='Wi-Fi'):
        self.interface = interface
        # self.display_filter = display_filter - NOTE: Removed this filter to capture all packets
        self.capture = pyshark.LiveCapture(interface=interface)
        self.capture_thread = None
        self.is_capturing = False
        self._display_packets = False
        self.restart_timer = None  # Timer for thread restart
        self.connection_attempts = {}  # Dictionary to track connection attempts

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

    def _capture_packets(self):
        for packet in self.capture.sniff_continuously(packet_count=0):
            if not self.is_capturing:
                break   
            #------------------------------------------------------------------------------------#
            # Packet information
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            if 'IP' in packet:
                src = packet.ip.src
                dst = packet.ip.dst

                if 'TCP' in packet:
                    protocol = 'TCP'
                    packet_length = int(packet.length)
                    flags = packet.tcp.flags

                    if 'SYN' in flags:
                        description = 'TCP Handshake SYN'
                    else:
                        description = 'Other TCP Packet'
                elif 'UDP' in packet:
                    protocol = 'UDP'
                    packet_length = int(packet.length)
                    description = 'UDP Packet'
                elif 'ICMP' in packet:
                    protocol = 'ICMP'
                    packet_length = int(packet.length)
                    description = 'ICMP Packet'
                elif 'ARP' in packet:
                    protocol = 'ARP'
                    packet_length = int(packet.length)
                    description = 'ARP Packet'
                elif 'HTTP' in packet:
                    protocol = 'HTTP'
                    packet_length = int(packet.length)
                    description = 'HTTP Packet'
                else:
                    protocol = 'Other'
                    packet_length = int(packet.length)
                    description = "Unknown/Other Protocol"
                
                # Displaying packet information for debugging purposes
                # print(f"Time: {time}, Source: {src}, Destination: {dst}, Protocol: {protocol}, Length: {packet_length}, Description: {description}")
            #------------------------------------------------------------------------------------#
            
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

            