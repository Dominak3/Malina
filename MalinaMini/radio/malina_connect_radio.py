import os
import time

# Název vašich AirPods
airpods_name = "AirPods"

def run_command(command):
    result = os.popen(command).read()
    return result

def connect_airpods():
    # Zapnutí Bluetooth
    os.system("sudo systemctl start bluetooth")

    # Zapnutí režimu párování
    os.system("bluetoothctl -- power on")
    os.system("bluetoothctl -- agent on")
    os.system("bluetoothctl -- default-agent")
    os.system("bluetoothctl -- scan on")

    # Vyhledání AirPods
    time.sleep(10)  # Čekání na nalezení zařízení

    # Získání seznamu zařízení
    devices = run_command("bluetoothctl devices")

    # Vyhledání MAC adresy AirPods
    mac_address = None
    for line in devices.split("\n"):
        if airpods_name in line:
            mac_address = line.split(" ")[1]
            break

    if mac_address:
        # Párování a připojení k AirPods
        os.system(f"bluetoothctl -- pair {mac_address}")
        os.system(f"bluetoothctl -- connect {mac_address}")
        os.system(f"bluetoothctl -- trust {mac_address}")
        return "AirPods connected."
    else:
        return "AirPods not found."