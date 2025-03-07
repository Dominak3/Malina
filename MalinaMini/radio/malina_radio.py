import vlc
import time

# URL rádia
radio_url = "https://stream.rcs.revma.com/asn0cmvb938uv"

# Vytvoření instance přehrávače
player = vlc.MediaPlayer(radio_url)

def play_radio():
    player.play()

def stop_radio():
    player.stop()
