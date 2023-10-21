# Install,Import and check all the required dependencies necessary for LIDS-CLI to run and conduct packet analysis
import os
import sys
import shutil
import subprocess


def check_dependencies():
    """
    Install and Import and check all dependencies necessary for LIDS-CLI to run
    and conduct packet analysis
    """
    dependencies = ["pyshark", "scapy"]

    try:
        import pyshark
        import scapy
    except ImportError:
        for dependency in dependencies:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", dependency],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                )
            except Exception as e:
                print(f"Error installing {dependency}: {e}")
                sys.exit(1)
        try:
            import pyshark
            import scapy
        except ImportError:
            print("Error importing dependencies")
            sys.exit(1)


def find_wireshark():
    """
    Attempts to find the Wireshark executable in the system's PATH.
    Returns the path to the executable if found, otherwise None.
    """
    possible_executables = ["wireshark", "Wireshark.exe"]

    for executable in possible_executables:
        try:
            executable_path = shutil.which(executable)
        except AttributeError:
            executable_path = None
            for path in os.environ["PATH"].split(os.pathsep):
                # Check if the program exists in this directory.
                if os.path.exists(os.path.join(path, executable)):
                    executable_path = executable
                    break
        # Return the full path to the executable file.
        if executable_path:
            #print(f"Wireshark executable found at {executable_path}")
            return executable_path
    print("Wireshark executable not found\nplease install Wireshark and try again")
    return None


def are_dependencies_satisfied():
    """
    Checks if all necessary dependencies are satisfied.
    Returns True if all dependencies are satisfied, otherwise False.
    """
    # Check Python dependencies
    try:
        import pyshark
        import scapy
    except ImportError:
        check_dependencies()
        try:
            import pyshark
            import scapy
        except ImportError:
            return False

    # Check Wireshark installation
    if not find_wireshark():
        return False
    return True


# check_dependencies()
# find_wireshark()
are_dependencies_satisfied()
