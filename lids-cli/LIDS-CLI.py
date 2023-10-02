import os, sys, re
import subprocess
from socket import socket, AF_INET, SOCK_STREAM
from LIDS_Agent import ingestConfig
import pyshark
import threading


# ANSI escape code for text color
red_text = "\033[31mRed Text\033[0m"  # Red text, followed by a reset code to return to the default color
green_text = "\033[32mGreen Text\033[0m"  # Green text, followed by a reset code
yellow_text = "\033[33mYellow Text\033[0m"  # Yellow text, followed by a reset code
sys.ps1 = "~ " 

# Dictionary of commands and their descriptions
commands_help = {"start": "Start the LIDS Program",
                "stop": "Stop the LIDS Program",
                "quit": "Exit LIDS",
                "help": "Display help for commands",
                "config": "Configure the LIDS Program with an XML file",
                "dpcap": "Display the most recent pcap",
                "dalerts": "Display alerts",
                "dalert": "Display a specific alert",
                "spcap": "Stop displaying pcaps"}

def open_pcap_file(pcap_file_path):
    try:
        # Launch Wireshark with the provided PCAP file path
        subprocess.Popen(["wireshark", pcap_file_path])
    except FileNotFoundError:
        print("Wireshark is not installed or not in your system's PATH.")
    except Exception as e:
        print(f"Error opening PCAP file: {str(e)}")

class PacketCapture:
    def __init__(self, interface='Wi-Fi', display_filter='tcp'):
        self.interface = interface
        self.display_filter = display_filter
        self.capture = pyshark.LiveCapture(interface=interface)
        self.capture_thread = None
        self.is_capturing = False
        self._display_packets = False

    def start_capture(self):
        if not self.is_capturing:
            print("Packet capture started in the background.")
            self.is_capturing = True
            self.capture_thread = threading.Thread(target=self._capture_packets)
            self.capture_thread.start()

    def stop_capture(self):
        if self.is_capturing:
            self.is_capturing = False
            self.capture_thread.join()
            print("Packet capture stopped.")

    def _capture_packets(self):
        for packet in self.capture.sniff_continuously(packet_count=0):
            if not self.is_capturing:
                break
            print(packet)

 

def main():
    # Create an instance of PacketCapture
    packet_capture = PacketCapture(interface="Wi-Fi")
    # Flag to track if packet capture is active
    capturing = False 

    # Displaying welcome message
    os.write(1, "Welcome to \033[31mLIDS\033[0m\n".encode())
    while(True):
        try:
            # Use os.write(1,f"Your Text {Variable}".encode()) to display text in terminal
            # Use os.read(0,800).decode() to read user input
                        
            # Displaying ~ in terminal
            os.write(1,f"{sys.ps1}".encode()) 
            # Reading user input
            user_input = os.read(0,800).decode().strip().lower()
            
            # Empty user input
            if len(user_input) == 0:
                continue
            
            # Stopping LIDS        
            if user_input == "quit":
                exit(0)
                
            # Displaying help
            if user_input == "help":
                for commands, description in commands_help.items():
                    os.write(1, f"{commands}:\t {description}\n".encode())
                os.write(1, f"\033[32mLOW - Low security risk labeled in green\033[0m\n".encode())
                os.write(1,f"\033[33mMEDIUM - Moderate security risk labeled in yellow\033[0m\n".encode())
                os.write(1,f"\033[31mHIGH - High security risk labeled in red\033[0m\n".encode())
                continue
            
            # Starting packet capture
            if user_input == "start":
                os.write(1, f"Starting LIDS...\n".encode())
                packet_capture.start_capture()
                continue
            
            # Stopping packet capture
            if user_input == "stop":
                os.write(1, f"Stopping LIDS...\n".encode())
                packet_capture.stop_capture()
                continue
            
            # Configuring LIDS
            if user_input == "config":
                os.write(1, f"Please enter path to configuration file\n".encode())
                configFile = os.read(0,800).decode().strip()
                # Check if the method returns true, if so the config file was ingested successfully
                ingestedSuccessfully = ingestConfig(configFile)
                if ingestedSuccessfully == True:
                    os.write(1, f"Configuration file loaded successfully\n".encode())
                continue
            
            # Displaying packet capture
            if user_input == "dpcap":
                os.write(1, f"Displaying PCAPS...\n".encode())
                packet_capture.display_packets()
                continue
            
            # Stopping packet capture
            if user_input == "spcap":
                os.write(1, f"Stopping PCAPS...\n".encode())
                packet_capture.stop_capture()
                continue
            
            # Displaying all alerts
            if user_input == "dalerts":
                os.write(1, f"Displaying alerts...\n".encode())
                continue
            
            # Displaying a specific alert
            if user_input == "dalert":
                os.write(1, f"Displaying alert...\n".encode())
                continue
            
            # If user input is not a command, display invalid command message
            else:
                os.write(1, f"Invalid command: '{user_input}' type 'help' for commands.\n".encode())
                continue
            
        except OSError:
            os.write(1, f"Error\n".encode())
        
if __name__ == "__main__":
    main()
