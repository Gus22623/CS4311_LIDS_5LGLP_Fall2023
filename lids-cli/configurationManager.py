import os
import configparser
import sys
from dependencyManager import find_wireshark


config_file = "configuration_settings.ini"
settings_configurer = configparser.ConfigParser()
wireshark_executable_location = ""
saved_pcap_directory = "/Users/alanochoa/Desktop/pcap_captures/"
xml_config_file_location = ""


def load_config_settings():
    """Load the configuration file settings."""
    global wireshark_executable_location
    try:
        settings_configurer.read(config_file)
        wireshark_executable_location = find_wireshark()
    except configparser.Error:
        print("Configuration File Error: {}".format(sys.exc_info()[1]))
        sys.exit(1)


def get_configuration_file_location():
    try:
        path = os.getcwd()
        if os.path.exists(config_file):
            return os.path.join(path, config_file)
        else:
            return ""
    except Exception as ex:
        print(
            "Something went wrong when getting the configuration file location: "
            + str(ex)
        )
    return ""


def read_configuration_file():
    if not os.path.exists(config_file):
        write_configuration_file()
    settings_configurer.read(config_file)
    if len(settings_configurer.sections()) == 0:
        settings_configurer.remove_section("default")
        settings_configurer.add_section("default")
        settings_configurer.set("default", "config_file", config_file)
        write_configuration_file()
    return settings_configurer


def ensure_settings_exist():
    if not os.path.exists(config_file):
        write_configuration_file()


def write_configuration_file():
    if not os.path.exists(config_file):
        settings_configurer.add_section("SETTINGS")
    settings_configurer.set("SETTINGS", "WIRESHARK_LOC", wireshark_executable_location)
    settings_configurer.set("SETTINGS", "PCAP_DIR", saved_pcap_directory)
    settings_configurer.set("SETTINGS", "CAPTURE_INTERVAL", "120")
    settings_configurer.set("SETTINGS", "CONFIG_XML_LOC", "")
    with open(config_file, "w") as config_file_handle:
        settings_configurer.write(config_file_handle)
    print(
        "Setting changes can be made in {} using a text editor.\n".format(config_file)
    )


def set_configuration_item(setting, value):
    try:
        read_configuration_file()
        settings_configurer.set("SETTINGS", setting, value)
        with open(config_file, "w") as config_file_handle:
            settings_configurer.write(config_file_handle)
    except (
        OSError,
        configparser.NoSectionError,
        configparser.NoOptionError,
        configparser.DuplicateSectionError,
        configparser.DuplicateOptionError,
    ) as e:
        print(f"Configuration Error: {e}")


def get_configuration_item(setting):
    read_configuration_file()
    if "SETTINGS" in settings_configurer:
        if setting in settings_configurer["SETTINGS"]:
            return settings_configurer["SETTINGS"][setting]
        else:
            raise KeyError("Setting not found in configuration file.")
    else:
        raise KeyError("Settings section not found in configuration file.")


def print_configuration_settings():
    read_configuration_file()
    if settings_configurer is None:
        print("There is no configuration file to read.\n")
        return
    print("Current settings:")
    for setting in settings_configurer["SETTINGS"]:
        print(f"{setting} = {settings_configurer['SETTINGS'][setting]}")
    print("\n")


# Load the configuration settings on module import
load_config_settings()
