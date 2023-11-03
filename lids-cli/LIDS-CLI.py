###########################################################
# @author
# @version
###########################################################

import os, sys, re
import socket
from socket import socket, AF_INET, SOCK_STREAM
from LIDS_Agent import test
from LIDS_Agent import ingestConfig


# ANSI escape code for text color
# Use these as a reference in case you want to use colored text in your code
red_text = "\033[31mRed Text\033[0m"  # Red text, followed by a reset code to return to the default color
green_text = "\033[32mGreen Text\033[0m"  # Green text, followed by a reset code
yellow_text = "\033[33mYellow Text\033[0m"  # Yellow text, followed by a reset code
sys.ps1 = "~ " 

# Dictionary of commands and their descriptions
commands_help = {"start": "Start the LIDS Program",
                "stop": "Stop the LIDS Program",
                "quit": "Exit LIDS",
                "help": "Display help for commands",
                "configure": "Configure the LIDS Program with an XML file",
                "display PCAPS": "Display the most recent pcap",
                "display alerts": "Display alerts",
                "display alert": "Display a specific alert"}


def main():
    # Displaying welcome message
    os.write(1, "Welcome to \033[31mLIDS\033[0m\n".encode())
    while(True):
        try:
            # Displaying ~ in terminal
            os.write(1,f"{sys.ps1}".encode()) 
            # Reading user input
            user_input = os.read(0,800).decode().strip().lower()
            # User input is empty
            if len(user_input) == 0:
                continue
            # User input is quit         
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
            if user_input == "start":
                os.write(1, f"Starting LIDS...\n".encode())
                continue
            if user_input == "stop":
                os.write(1, f"Stopping LIDS...\n".encode())
                continue
            if user_input == "configure":
                os.write(1, f"Please enter path to configuration file\n".encode())
                configFile = os.read(0,800).decode().strip()
                temp = ingestConfig(configFile)
                
                continue
            if user_input == "display pcaps":
                os.write(1, f"Displaying PCAPS...\n".encode())
                continue
            if user_input == "display alerts":
                os.write(1, f"Displaying alerts...\n".encode())
                continue
            else:
                os.write(1, f"Invalid command: '{user_input}' type 'help' for commands.\n".encode())
                continue
        except OSError:
            os.write(1, f"Error\n".encode())
        
if __name__ == "__main__":
    main()
