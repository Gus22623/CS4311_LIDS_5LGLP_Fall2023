# LIDS-CLI.py: A command line interface for the LIDS program
import os
import sys
from datetime import datetime


from dependencyManager import check_dependencies
from configurationManager import (
    load_config_settings,
    get_configuration_file_location,
    read_configuration_file,
    ensure_settings_exist,
    write_configuration_file,
    set_configuration_item,
    get_configuration_item,
    print_configuration_settings,
)

from LIDS_Agent import PacketCapture
from LIDS_Agent import config
from LIDS_Agent import open_pcap_file, display_pcap_file


# Dictionary of commands and their descriptions
commands_help = {
    "start": "Start the LIDS Program",
    "stop": "Stop the LIDS Program",
    "quit": "Exit LIDS",
    "help": "Display help for commands",
    "config": "Configure the LIDS Program with an XML file",
    "dpcap": "Display the most recent pcap",
    "dalerts": "Display alerts",
    "dalert": "Display a specific alert",
    "spcap": "Stop displaying pcaps",
}

# settingConfigrations = configSettings.read_configuration_file()


# Display program commands on user request
def display_help():
    os.write(1, f"\n".encode())
    max_command_length = (
        max(len(command) for command in commands_help.keys()) + 1
    )  # +1 for the colon
    for command, description in commands_help.items():
        formatted_command = f"{command}:".ljust(max_command_length)
        os.write(1, f"{formatted_command} {description}\n".encode())
    os.write(1, f"\n{'-------------- Alert Severity Levels --------------'}\n".encode())
    os.write(
        1, f"\033[32m{'LOW':<6} - Low security risk labeled in green\033[0m\n".encode()
    )
    os.write(
        1,
        f"\033[33m{'MEDIUM':<6} - Moderate security risk labeled in yellow\033[0m\n".encode(),
    )
    os.write(
        1, f"\033[31m{'HIGH':<6} - High security risk labeled in red\033[0m\n".encode()
    )


# Displaying commands on startup
def display_commands():
    os.write(1, f"\nEnter a Command:\n".encode())
    for command, description in commands_help.items():
        os.write(1, f"{command}:\t {description}\n".encode())


# Main function
def main():
    # Set the prompt to ~
    sys.ps1 = "~ "
    # Create an instance of PacketCapture
    packet_capture = PacketCapture(interface="Wi-Fi")
    # Flag to track if packet capture is active
    capturing = False

    # Displaying welcome message
    os.write(1, "\nWelcome to \033[31mLIDS\033[0m\n".encode())
    display_commands()
    while True:
        try:
            # Use os.write(1,f"Your Text {Variable}".encode()) to display text in terminal
            # Use os.read(0,800).decode() to read user input

            # Displaying ~ in terminal
            os.write(1, f"{sys.ps1}".encode())
            # Reading user input
            user_input = os.read(0, 800).decode().strip().lower()

            # Empty user input
            if len(user_input) == 0:
                continue

            # Stopping LIDS
            if user_input == "quit":
                exit(0)

            # Displaying help
            if user_input == "help":
                # os.system('cls' if os.name == 'nt' else 'clear')
                display_help()
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
                xml_part = None
                if os.path.exists(get_configuration_file_location()):
                    # Load existing configuration if .ini file exists
                    config_data = read_configuration_file()
                    if (
                        "SETTINGS" in config_data
                        and "CONFIG_XML_LOC" in config_data["SETTINGS"]
                    ):
                        xml_part = config_data["SETTINGS"]["CONFIG_XML_LOC"]

                if not xml_part:
                    # If xml_part is not set in the .ini file, prompt the user for input
                    os.write(
                        1, f"Please enter path to xml configuration file\n".encode()
                    )
                    xml_part = os.read(0, 800).decode().strip()

                xml_Config = config()
                ingestedSuccessfully = xml_Config.ingestConfig(xml_part)
                if ingestedSuccessfully:
                    os.write(1, f"Configuration file loaded successfully\n".encode())
                    set_configuration_item("CONFIG_XML_LOC", xml_part)
                    #print_configuration_settings() # configuration debugging step
                else:
                    os.write(1, f"Configuration file failed to load\n".encode())
                continue

            # Displaying packet capture
            if user_input == "dpcap":
                os.write(1, f"Please enter path to pcap file\n".encode())
                os.write(
                    1,
                    f"Example: /home/user/Desktop/pcap.pcapng\n".encode(),  # Windows example: C:\\Users\\User\\Desktop\\pcap.pcapng
                )
                pcapFile = os.read(0, 800).decode().strip()
                display_pcap_file(pcapFile)
                # open_pcap_file(pcapFile)
                continue

            # Displaying all alerts
            if user_input == "dalerts":
                os.write(1, f"Displaying alerts...\n".encode())
                continue

            # Displaying a specific alert
            if user_input == "dalert":
                os.write(1, f"Displaying alert...\n".encode())
                continue

            # clear the terminal screen
            if user_input == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                continue

            # If user input is not a command, display invalid command message
            else:
                os.write(
                    1,
                    f"Invalid command: '{user_input}' type 'help' for commands.\n".encode(),
                )
                continue

        except OSError:
            os.write(1, f"Error\n".encode())


# Main function call
if __name__ == "__main__":
    check_dependencies()
    load_config_settings()
    main()
