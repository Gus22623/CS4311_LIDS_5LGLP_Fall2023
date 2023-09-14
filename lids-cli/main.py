from configure import configure_agent
from displayPCAP import pcap_display_box, pcap_specific

def display_window(title, options):
    print(f"{'='*len(title)}")
    print(title)
    print(f"{'='*len(title)}")

    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

def main_menu():
    agent_info = None
    commands = ["Configure: Shows/SetsUp config file options",
                         "Display PCAP: Will Show the most recent pcap", 
                         "Display PCAP X: Will Show a specific pcap",
                         "Help: Show commands avaiable",
                         "Exit"]
    while True:
        display_window("The following are commands avaialble:", commands)
        choice = int(input("Enter your choice: "))

        if choice == 1:
            agent_info = configure_agent()
        elif choice == 2:
            pcap_display_box()
        elif choice == 3:
            source = input("Enter the source: ")
            pcap_specific(source)
        elif choice == 4:
            print()
            print("Available Commands are: \n", commands , "\n")
        elif choice == 5:
            break
        else:
            print("Invalid choice \n")

if __name__ == '__main__':
    main_menu()
