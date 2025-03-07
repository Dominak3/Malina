from nicegui import ui, app
from radio.malina_radio import play_radio, stop_radio
from radio.malina_connect_radio import connect_airpods
from recorder.malina_recorder import record_radio_with_backup, convert_raw_files_in_folder, combine_mp3_files, shutdown_or_restart_raspberry_pi, delete_files_in_folder
from system_info.system_info import get_system_info
import os
from pydub import AudioSegment
import subprocess
from datetime import datetime
import threading
import sys
import io
import time

# Set the path to ffmpeg and ffprobe
current_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = f"{current_dir}/ffmpeg"
ffplay_path = f"{current_dir}/ffplay"  # Full path to ffplay
AudioSegment.converter = ffmpeg_path
AudioSegment.ffprobe = f"{current_dir}/ffprobe"

# Function to display notifications
def show_message(message):
    ui.notify(message)

# Recording variables
radio_url = "https://stream.rcs.revma.com/asn0cmvb938uv"
temp_file_prefix = "temp_stream"
output_file_prefix = "recorded_radio"
raw_folder = "recorder/raw"
mp3_folder = "recorder/mp3"
recorded_folder = "recorder/recorded"

# Ensure directories exist
os.makedirs(raw_folder, exist_ok=True)
os.makedirs(mp3_folder, exist_ok=True)
os.makedirs(recorded_folder, exist_ok=True)

# Audio playback variables
player_process = None
paused_time = 0

def play_audio(file_path, start_time=0):
    global player_process, paused_time
    if player_process:
        player_process.terminate()
    player_process = subprocess.Popen([ffplay_path, "-nodisp", "-autoexit", "-ss", str(start_time), file_path])
    paused_time = start_time

def stop_audio():
    global player_process, paused_time
    if player_process:
        player_process.terminate()
        paused_time = 0
        player_process = None

def seek_audio(file_path, seconds):
    global player_process, paused_time
    if player_process:
        player_process.terminate()
        paused_time += seconds
        player_process = subprocess.Popen([ffplay_path, "-nodisp", "-autoexit", "-ss", str(paused_time), file_path])

app.add_static_files('/static', 'static')

# Redirect stdout to capture console output
console_output = io.StringIO()
sys.stdout = console_output

# Home page
@ui.page('/')
def home_page():
    ui.add_head_html("<meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'>")
    ui.add_head_html("<meta name='apple-mobile-web-app-capable' content='yes'>")
    ui.add_head_html("<meta name='apple-mobile-web-app-status-bar-style' content='black'>")
    ui.add_head_html("<link rel='shortcut icon' href='static/favicon.ico' type='image/x-icon' />")
    ui.add_head_html('<link rel="apple-touch-icon" href="static/apple-touch-icon.png">') 
    ui.add_head_html("<link rel='manifest' href='static/site.webmanifest'>")
    ui.add_head_html('<style>body {background-color: #f3f4f6; }</style>')
    with ui.column().classes('items-center w-full h-screen bg-gray-100 p-6'):
        ui.label('🍓 Malina 🍓').classes('text-4xl font-bold text-red-600 mb-6')
        
        with ui.column().classes('gap-6 w-full items-center'):
            for name, link in [('🎵 Online Rádio', '/radio'), ('🎙 Nahrávání', '/nahravani'), ('📁 Záznamy', '/zaznamy'), ('⚙️ Systém', '/system')]:
                ui.link(name, link).classes('bg-red-500 text-white text-xl px-6 py-3 rounded-lg hover:bg-red-600 w-4/5 max-w-sm text-center no-underline')

# Online Radio Page
@ui.page('/radio')
def radio_page():
    ui.add_head_html('<style>body {background-color: #f53911; }</style>')
    ui.add_head_html('<meta name="theme-color" content="#f53911" />')
    with ui.column().classes('items-center w-full h-screen bg-gray-100 p-6'):
        ui.label('🎵 Online Rádio').classes('text-3xl font-bold text-red-600 mb-6')
        
        with ui.column().classes('gap-4 w-full items-center'):
            ui.button('▶️ Přehrát', on_click=lambda: (play_radio(), show_message("Rádio spuštěno")), color="green").classes('bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600')
            ui.button('⏹️ Zastavit', on_click=lambda: (stop_radio(), show_message("Rádio zastaveno")), color="red").classes('bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600')
            ui.button('🎧 Připojit AirPody', on_click=lambda: (connect_airpods(), show_message("Připojování k AirPodům...")), color="blue").classes('bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600')
        
        ui.link('Zpět', '/').classes('bg-gray-500 text-white text-xl px-6 py-3 rounded-lg hover:bg-gray-600 mt-6 fixed bottom-4 no-underline')

# Recording Page
@ui.page('/nahravani')
def recording_page():
    ui.add_head_html('<style>body {background-color: #fc795d; }</style>')
    ui.add_head_html('<meta name="theme-color" content="#fc795d" />')
    with ui.column().classes('items-center w-full h-screen bg-gray-100 p-6'):
        ui.label('🎙 Nahrávání').classes('text-3xl font-bold text-red-600 mb-6')
        
        interval_input = ui.input('Interval (s)', value='900').classes('w-4/5 max-w-sm')
        total_duration_input = ui.input('Celková doba (s)', value='9000').classes('w-4/5 max-w-sm')
        shutdown_checkbox = ui.checkbox('Vypnout Raspberry Pi po nahrávání').classes('w-4/5 max-w-sm')
        
        def start_recording():
            record_radio_with_backup(radio_url, int(interval_input.value), int(total_duration_input.value), temp_file_prefix, output_file_prefix)
            show_message("Nahrávání spuštěno")
        
        ui.button('⏺ Spustit nahrávání', on_click=start_recording, color="red").classes('bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600')
        
        ui.link('Zpět', '/').classes('bg-gray-500 text-white text-xl px-6 py-3 rounded-lg hover:bg-gray-600 mt-6 fixed bottom-4 no-underline')

# Recordings Page
@ui.page('/zaznamy')
def recordings_page():
    ui.add_head_html('<style>body {background-color: #26d7ff; }</style>')
    ui.add_head_html('<meta name="theme-color" content="#26d7ff" />')
    with ui.column().classes('items-center w-full h-screen bg-gray-100 p-6'):
        ui.label('📁 Záznamy').classes('text-3xl font-bold text-red-600 mb-6')
        
        recorded_files = [f for f in os.listdir(recorded_folder) if f.endswith('.mp3')]
        for file_name in recorded_files:
            file_path = f"{recorded_folder}/{file_name}"
            with ui.row().classes('gap-2 w-full items-center justify-center'):
                ui.button("Pustit: "+file_name, on_click=lambda fp=file_path: play_audio(fp), color="pink").classes('text-pink-600 hover:no-underline')
                ui.button('⏪ 10s', on_click=lambda fp=file_path: seek_audio(fp, -10), color="pink").classes('text-pink-600 hover:no-underline')
                ui.button('⏩ 10s', on_click=lambda fp=file_path: seek_audio(fp, 10), color="pink").classes('text-pink-600 hover:no-underline')
                ui.button('⏹️ Zastavit', on_click=stop_audio, color="pink").classes('text-pink-600 hover:no-underline')
        
        ui.link('Zpět', '/').classes('bg-gray-500 text-white text-xl px-6 py-3 rounded-lg hover:bg-gray-600 mt-6 fixed bottom-4 no-underline')

# System Page
@ui.page('/system')
def system_page():
    ui.add_head_html('<style>body {background-color: #2a2a2a; }</style>')
    ui.add_head_html('<meta name="theme-color" content="#2a2a2a" />')
    system_info = get_system_info()
    with ui.column().classes('items-center w-full h-screen bg-gray-100 p-6'):
        ui.label('⚙️ Systém').classes('text-3xl font-bold text-red-600 mb-6')
        
        ui.label(f"Model: {system_info['model']}").classes('text-lg text-gray-700')
        ui.label(f"Python Version: {system_info['python_version']}").classes('text-lg text-gray-700')
        ui.label(f"IP Address: {system_info['ip_address']}").classes('text-lg text-gray-700')
        ui.label(f"Temperature: {system_info['temperature']}").classes('text-lg text-gray-700')
        ui.label(f"CPU Usage: {system_info['cpu_usage']}").classes('text-lg text-gray-700')
        ui.label(f"Memory Usage: {system_info['memory_usage']}").classes('text-lg text-gray-700')
        ui.label(f"Disk Usage: {system_info['disk_usage']}").classes('text-lg text-gray-700')
        
        ui.link('Zpět', '/').classes('bg-gray-500 text-white text-xl px-6 py-3 rounded-lg hover:bg-gray-600 mt-6 fixed bottom-4 no-underline')

# Run UI
ui.run(title='Malina')
