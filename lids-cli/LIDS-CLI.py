# LIDS-CLI.py: A command line interface for the LIDS program

import os, sys
from datetime import datetime
from LIDS_Agent import PacketCapture
from LIDS_Agent import ingestConfig
from LIDS_Agent import open_pcap_file

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

# Main function
def main():
    # Set the prompt to ~
    sys.ps1 = "~ " 
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
                os.write(1, f"Please enter path to pcap file\n".encode())
                os.write(1, f"Example: C:\\Users\\User\\Desktop\\pcap.pcapng\n".encode())
                pcapFile = os.read(0,800).decode().strip()
                open_pcap_file(pcapFile)
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
            
# Main function call      
if __name__ == "__main__":
    main()
