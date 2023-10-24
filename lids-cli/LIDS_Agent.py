# LIDS_Agent back end code.
import os
import threading
import subprocess

import xml.etree.ElementTree as ET
from scapy.all import *
from datetime import datetime
import pyshark

from db import cursor, db
from prettytable import PrettyTable
from dependencyManager import find_wireshark


class config:
    def __init__(self):
        self.configurations = {}  # Dictionary to store configurations

    def ingestConfig(self, configFile):
        try:
            # Parse the XML data
            root = ET.fromstring(configFile)
            for system in root.findall("system"):
                name = system.find("name").text
                ip = system.find("ip").text
                mac = system.find("mac").text
                ports = system.find("ports").text
                whitelist = system.find("whitelist").text

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


# def connectToServer():
#     import socket

#     # Create a socket object
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # Define the server's IP address and port
#     server_ip = 'your_server_ip_here'
#     server_port = 12345  # Use the same port as the server

#     try:
#         # Connect to the server
#         client_socket.connect((server_ip, server_port))
#         print("Connected to the server.")

#         # Send data to the server
#         message = "LIDS connected successfully."
#         client_socket.send(message.encode())

#         # Receive data from the server
#         data = client_socket.recv(1024)  # Adjust the buffer size as needed
#         print(f"Received from server: {data.decode()}")

#     except ConnectionRefusedError:
#         print("Connection to the server was refused. Make sure the server is running.")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

#     finally:
#         # Close the client socket
#         client_socket.close()


# Class to handle packet capture
class PacketCapture:
    def __init__(self, interface="Wi-Fi"):
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

            # ------------------------------------------------------------------------------------#
            # Packet information
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            if "IP" in packet:
                src = packet.ip.src
                dst = packet.ip.dst

                if "TCP" in packet:
                    protocol = "TCP"
                    packet_length = int(packet.length)
                    flags = packet.tcp.flags

                    if "SYN" in flags:
                        description = "TCP Handshake SYN"
                    else:
                        description = "Other TCP Packet"
                elif "UDP" in packet:
                    protocol = "UDP"
                    packet_length = int(packet.length)
                    description = "UDP Packet"
                elif "ICMP" in packet:
                    protocol = "ICMP"
                    packet_length = int(packet.length)
                    description = "ICMP Packet"
                elif "ARP" in packet:
                    protocol = "ARP"
                    packet_length = int(packet.length)
                    description = "ARP Packet"
                elif "HTTP" in packet:
                    protocol = "HTTP"
                    packet_length = int(packet.length)
                    description = "HTTP Packet"
                else:
                    protocol = "Other"
                    packet_length = int(packet.length)
                    description = "Unknown/Other Protocol"

                """
                NOTE:Displaying packet information for debugging purposes
                Uncomment the following line to display packet information
                | |
                V V
                """
                # Create a dictionary to represent the packet
                packet_info = {
                    "Time": time,
                    "Source": src,
                    "Destination": dst,
                    "Protocol": protocol,
                    "Length": packet_length,
                    "Description": description,
                }

                # Pass the packet information to detect_alert method
                self.detect_alert(packet_info)

                # print(f"Time: {time}, Source: {src}, Destination: {dst}, Protocol: {protocol}, Length: {packet_length}, Description: {description}")
            # ------------------------------------------------------------------------------------#
            # TODO: Implement packet analysis logic here

    # ------------------------------------------------------------------------------------#

    # Method to detect alerts
    def detect_alert(self, packet):
        if "IP" in packet:
            src = packet.ip.src
            dst = packet.ip.dst

            # Check for Port Scan
            if "TCP" in packet:
                dst_port = int(packet.tcp.dstport)
                cursor.execute(
                    f"SELECT * FROM config WHERE ip = '{dst}' AND FIND_IN_SET({dst_port}, ports)"
                )
                result = cursor.fetchone()
                if result is None:
                    self.trigger_alert(packet, "Port Scan", "Medium")

            # Check for Failed Login Attempt
            if "TCP" in packet:
                src_port = int(packet.tcp.srcport)
                cursor.execute(
                    f"SELECT * FROM config WHERE ip = '{src}' AND FIND_IN_SET({src_port}, ports)"
                )
                result = cursor.fetchone()
                if result is not None:
                    self.trigger_alert(packet, "Failed Login Attempt", "High")

            # Check if the source or destination IP is Whitelisted
            cursor.execute(
                f"SELECT * FROM config WHERE (ip = '{src}' AND FIND_IN_SET('{dst}', whitelist)) OR (ip = '{dst}' AND FIND_IN_SET('{src}', whitelist))"
            )
            result = cursor.fetchone()
            if result is not None:
                return

            # If none of the above conditions are met, trigger a default alert
            self.trigger_alert(packet, "Unknown Activity", "Low")

    # ------------------------------------------------------------------------------------#

    def trigger_alert(self, packet, alert_type, severity):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        src = packet.ip.src
        dst = packet.ip.dst
        protocol = "Unknown"
        if "TCP" in packet:
            protocol = "TCP"
        elif "UDP" in packet:
            protocol = "UDP"
        # Add more protocol checks if needed

        # Map severity to level
        level = 0
        if severity == "High":
            level = 3
        elif severity == "Medium":
            level = 2
        elif severity == "Low":
            level = 1

        try:
            # Insert the alert into the 'alerts' table
            cursor.execute(
                "INSERT INTO alerts (Lvl, Time, IP, Port, Description) VALUES (%s, %s, %s, %s, %s)",
                (level, time, src, dst, alert_type),
            )
            db.commit()

            print(
                f"ALERT [{severity}]: {alert_type} detected and saved to the database."
            )
            print(
                f"Time: {time}, Source: {src}, Destination: {dst}, Protocol: {protocol}"
            )

        except Exception as e:
            print(f"Error occurred while saving alert to database: {e}")

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


class Alerts:
    def __init__(self):
        self.cursor = cursor

    def getAlerts(self):
        try:
            # Fetch data from the 'alerts' table
            self.cursor.execute(
                "SELECT level, time, source_ip, port, description FROM alert"
            )
            alerts = self.cursor.fetchall()

            # Convert data to a list of dictionaries for JSON response
            alerts_data = [
                {
                    "level": alert[0],
                    "time": alert[1],
                    "source_ip": alert[2],
                    "port": alert[3],
                    "desc": alert[4],
                }
                for alert in alerts
            ]

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
                table.add_row(
                    [
                        alert["level"],
                        alert["time"],
                        alert["source_ip"],
                        alert["port"],
                        alert["desc"],
                    ]
                )

            return str(table)
        else:
            return f"Error: {alerts}"
