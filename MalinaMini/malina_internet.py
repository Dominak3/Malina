import os
import time

# Název a heslo vaší Wi-Fi sítě
wifi_ssid = "Home_stastny"
wifi_psk = "dominik08"

# Název a heslo vašeho hotspotu
hotspot_ssid = "Kristýna - iPhone 16 Pro"
hotspot_psk = "heslokiki1"

# Funkce pro kontrolu připojení k Wi-Fi síti
def is_wifi_connected():
    result = os.popen("iwgetid -r").read().strip()
    return result != ""

# Funkce pro připojení k Wi-Fi síti
def connect_to_wifi(ssid, psk):
    wpa_supplicant_conf = f"""
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=CZ

    network={{
        ssid="{ssid}"
        psk="{psk}"
        key_mgmt=WPA-PSK
    }}
    """
    wpa_supplicant_path = "/etc/wpa_supplicant/wpa_supplicant.conf"
    with open(wpa_supplicant_path, "w") as file:
        file.write(wpa_supplicant_conf)
    os.system("sudo wpa_cli -i wlan0 reconfigure")
    time.sleep(10)  # Čekání na připojení k síti

# Pokud není připojení k Wi-Fi, připojit se k hotspotu
if not is_wifi_connected():
    print("Wi-Fi network not found, connecting to hotspot...")
    connect_to_wifi(hotspot_ssid, hotspot_psk)
    if is_wifi_connected():
        print("Connected to hotspot.")
    else:
        print("Failed to connect to hotspot.")
else:
    print("Wi-Fi network is already connected.")