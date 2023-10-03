import os, sys, re
import xml.etree.ElementTree as ET
import threading
from socket import socket, AF_INET, SOCK_STREAM

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
    
def manageConnections():
     # Get server IP and port number of LIDS-D
    host = input("Provide server IP: ").strip()
    port = int(input("Provide server port #: ").strip())

    # Create socket LIDS-D to allow LIDS clients to connect to it
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((host, port))

    print("HostName: ", host)
    print("Socket created and bound to port: ", port)

    # Allow LIDS-D to listen for connections
    serverSocket.listen(5)
    print("Server started and listening for connections...")

    while True:
        # Accept connection from LIDS client
        clientSocket, addr = serverSocket.accept()
        print("Connection from: " + str(addr))
        print()

        # Start a new thread and return its identifier
        t = threading.Thread(target=clientHandler, args=(clientSocket, port))
        t.start()

    # Close connection
    serverSocket.close()
    
# Allow LIDS-D to receive alerts from multiple LIDS clients
# and print the reports to the terminal
def clientHandler(c, port):
    # while client is connected to LIDS-D
    while True:
        # Receive data from LIDS client
        data = c.recv(1024)
        if not data:
            print("Client disconnected")
            break

        # Print data to terminal
        print("Received from LIDS client: " + str(data.decode()))

        # Send data back to LIDS client
        c.send(data)

    # Close connection with client if client disconnects
    c.close()