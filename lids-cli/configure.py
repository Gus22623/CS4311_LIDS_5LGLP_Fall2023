def configure_agent():
    name = input("Enter Agent Name: ")
    ip = input("Enter Agent IP Address: ")
    mac = input("Enter Agent MAC Address: ")
    port = input("Enter Agent Port: ")

    # save into DB
    return {'Name': name, 'IP Address': ip, 'MAC Address': mac, 'Port': port}
