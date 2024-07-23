import subprocess
import platform
import sys

def ping(host):
    # Determine the correct option based on the operating system
    print(f"Detected system: {sys.platform}")
    if sys.platform == "win32":
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        try:
            # Run the ping command
            result = subprocess.run(['ping', param, '4', host], capture_output=True, text=True, check=True)
            print(result.stdout)
            return 0
        except subprocess.CalledProcessError as e:
            print(f"Ping failed: {e}")
            return e.returncode
        except PermissionError as e:
            print(f"Access denied. Try running the script with administrative privileges. {e}")
            return -1
    elif "linux" in sys.platform:
        print("Linux ping function not tested yet")
                # Run the ping command
        result = subprocess.run(['ping', '-c', '4', host], capture_output=True, text=True)

        # Print the output of the ping command
        print(result.stdout)

        # Return the return code (0 means success)
        return result.returncode
    else:
        print("Unknown system.platform: %s  Installation failed, see setup.py." % sys.platform)
        sys.exit(1)

# Example usage
ping_result = ping('192.168.54.172')
if ping_result == 0:
    print("Ping was successful")
else:
    print("Ping failed")
