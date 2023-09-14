from configure import configure_agent
from displayPCAP import pcap_display_box
from displayAlert import alert_display_box

def display_window(title, options):
    print(f"{'='*len(title)}")
    print(title)
    print(f"{'='*len(title)}")

    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

def main_menu():
    agent_info = None
    
    while True:
        display_window("Main Menu", ["Configure", "Display PCAP Files","Display Alerts", "Exit"])
        choice = int(input("Enter your choice: "))

        if choice == 1:
            agent_info = configure_agent()
        elif choice == 2:
            pcap_display_box()
        elif choice == 3:
            alert_display_box()
        elif choice == 4:
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main_menu()
