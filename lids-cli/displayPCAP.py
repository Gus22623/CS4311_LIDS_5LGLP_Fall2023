def pcap_display_box():

    print()
    print("Info: Showing most recent PCAP")
    print(f"{'='*100}")
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format("Time", "Source", "Destination", "Protocol", "Length", "Description"))
    print(f"{'='*100}")
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<30}".format("5:05", "192.1.0.2", "192.0.0.1","TCP", "64", "PlaceHolder"))
    print(f"{'='*100}")
    print()

def pcap_specific(source):
    print()
    print("Info: Showing PCAP file from source:", source)
    print(f"{'='*100}")
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format("Time", "Source", "Destination", "Protocol", "Length", "Description"))
    print(f"{'='*100}")
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<30}".format("5:05", "192.1.0.2", "192.0.0.1","TCP", "64", "PlaceHolder"))
    print(f"{'='*100}")
    print()
