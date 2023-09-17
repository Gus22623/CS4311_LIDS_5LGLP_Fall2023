from scapy.all import sniff
from scapy.layers.inet import IP, TCP
# from cryptography.fernet import Fernet
import xml.etree.ElementTree as ET
import os, sys, re

#stigFile = {JSON file containing STIG rules}
configFile = None
#maliciousPackets = []
#alertList = []
#serverAddress = {IP address of server}
#serverPort = {Port of server}
#alert = {Alert String}

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

    except ET.ParseError:
        print("Error: Invalid XML file format.")
        main()
    except FileNotFoundError:
        print("Error: File not found.")
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        main()
        
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

def main():
    configFile = input("Enter the name of the configuration file: ")
    ingestConfig(configFile)
    
if __name__ == "__main__":
    main()