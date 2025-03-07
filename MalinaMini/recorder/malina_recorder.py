import requests
from pydub import AudioSegment
import time
import os
import re
from datetime import datetime

# Set the path to ffmpeg and ffprobe

current_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = f"{current_dir}/ffmpeg"
AudioSegment.converter = ffmpeg_path
AudioSegment.ffprobe = f"{current_dir}/ffprobe"

# Proměnné pro nahrávání
radio_url = "https://stream.rcs.revma.com/asn0cmvb938uv"
temp_file_prefix = "temp_stream"
raw_folder = "C:/Users/dominak3/Desktop/MalinaMini/recorder/raw"
recorded_folder = "C:/Users/dominak3/Desktop/MalinaMini/recorder/recorded"
mp3_folder = "C:/Users/dominak3/Desktop/MalinaMini/recorder/mp3"
combined_output_file = f"C:/Users/dominak3/Desktop/MalinaMini/recorder/recorded/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"

# Ensure the directories exist
os.makedirs(raw_folder, exist_ok=True)
os.makedirs(recorded_folder, exist_ok=True)
os.makedirs(mp3_folder, exist_ok=True)

def record_radio_with_backup(radio_url, interval_duration, total_duration, temp_file_prefix, output_file_prefix):
    try:
        response = requests.get(radio_url, stream=True)
        total_intervals = total_duration // interval_duration

        for i in range(total_intervals):
            temp_file = f"{temp_file_prefix}_{i+1}.raw"
            temp_file_path = f"{raw_folder}/{temp_file}"
            with open(temp_file_path, "wb") as f:
                start_time = time.time()
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
                    if time.time() - start_time > interval_duration:
                        break

            output_file_path = f"{raw_folder}/{temp_file}"
            os.rename(temp_file_path, output_file_path)
    except Exception as e:
        print(f"Error in record_radio_with_backup: {e}")

def convert_raw_files_in_folder(folder_path, output_folder):
    """
    Converts all raw audio files in a specified folder to mp3 format in numerical order.
    
    :param folder_path: Path to the folder containing raw files
    :param output_folder: Path to the folder to save the converted mp3 files
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    raw_files = [f for f in os.listdir(folder_path) if f.endswith(".raw")]
    raw_files.sort(key=lambda f: int(re.search(r'\d+', f).group()))

    for file_name in raw_files:
        temp_file = f"{folder_path}/{file_name}"
        output_file = f"{output_folder}/{file_name.replace('.raw', '.mp3')}"
        audio_segment = AudioSegment.from_file(temp_file, format="raw", frame_rate=44100, channels=2, sample_width=2)
        audio_segment.export(output_file, format="mp3")
        print(f"Converted {temp_file} to {output_file}")

def combine_mp3_files(input_folder, output_file):
    """
    Combines all mp3 files in a specified folder into a single mp3 file.
    
    :param input_folder: Path to the folder containing mp3 files
    :param output_file: Path to the output mp3 file
    """
    combined = AudioSegment.empty()
    
    mp3_files = [f for f in os.listdir(input_folder) if f.endswith('.mp3')]
    mp3_files.sort(key=lambda f: int(re.search(r'\d+', f).group()))

    for file_name in mp3_files:
        file_path = f"{input_folder}/{file_name}"
        audio = AudioSegment.from_mp3(file_path)
        combined += audio
    
    combined.export(output_file, format='mp3')
    print(f"Combined MP3 files from '{input_folder}' into '{output_file}'")

def delete_files_in_folder(folder_path):
    """
    Deletes all files in a specified folder.
    
    :param folder_path: Path to the folder to delete files from
    """
    for file_name in os.listdir(folder_path):
        file_path = f"{folder_path}/{file_name}"
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")

def shutdown_or_restart_raspberry_pi(shutdown=False):
    """
    Shuts down or restarts the Raspberry Pi.
    """
    if shutdown:
        os.system("sudo shutdown -h now")
    else:
        os.system("sudo reboot")

if __name__ == "__main__":
    interval_duration = 900  # Record each interval for 15 minutes (900 seconds)
    total_duration = 9000  # Total duration to record is 2.5 hours (9000 seconds)
    temp_file_prefix = "temp_stream"
    output_file_prefix = "recorded_radio"
    shutdown_after_recording = False  # Set this based on the checkbox selection
    restart_after_recording = True  # Set this based on the checkbox selection
    
    record_radio_with_backup(radio_url, interval_duration, total_duration, temp_file_prefix, output_file_prefix)
    convert_raw_files_in_folder(raw_folder, mp3_folder)
    combine_mp3_files(mp3_folder, combined_output_file)
    print(f"Combined file saved to {combined_output_file}")
    
    delete_files_in_folder(raw_folder)
    delete_files_in_folder(mp3_folder)
    
    if shutdown_after_recording:
        shutdown_or_restart_raspberry_pi(shutdown=True)
    elif restart_after_recording:
        shutdown_or_restart_raspberry_pi(shutdown=False)
