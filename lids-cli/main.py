import typer
from configure import configure_agent
from displayPCAP import pcap_display_box
from displayAlert import alert_display_box
from displayPCAP import pcap_specific

app = typer.Typer()

@app.command()
def configure():
    """
    Shows/Sets up config file options.
    """
    configure_agent()

@app.command()
def display_pcap():
    """
    Show the most recent pcap.
    """
    pcap_display_box()

@app.command()
def display_pcap_specific(source: str):
    """
    Show a specific pcap.

    Args:
        source (str): The source to display.
    """
    pcap_specific(source)

@app.command()
def display_alerts():
    """
    Display alerts.
    """
    alert_display_box()

def main():
    app()

if __name__ == "__main__":
    main()
