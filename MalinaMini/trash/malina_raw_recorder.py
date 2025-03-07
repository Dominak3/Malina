import requests
from pydub import AudioSegment
from io import BytesIO
import time
import os

# Set the path to ffmpeg and ffprobe
current_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(current_dir, 'ffmpeg')
AudioSegment.converter = ffmpeg_path
AudioSegment.ffprobe = os.path.join(current_dir, 'ffprobe')

def record_radio(url, duration, output_file):
    """
    Records online radio for a specified duration and saves it as an mp3 file.
    
    :param url: URL of the online radio stream
    :param duration: Duration to record in seconds
    :param output_file: Path to the output mp3 file
    """
    response = requests.get(url, stream=True)
    temp_file = "temp_stream.raw"

    with open(temp_file, "wb") as f:
        start_time = time.time()
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
            if time.time() - start_time > duration:
                break

    audio_segment = AudioSegment.from_file(temp_file, format="raw", frame_rate=44100, channels=2, sample_width=2)
    audio_segment.export(output_file, format="mp3")
    os.remove(temp_file)

def automate_recording(url, interval_duration, total_duration, output_file_prefix):
    """
    Automates the recording process for a specified number of intervals.
    
    :param url: URL of the online radio stream
    :param interval_duration: Duration of each recording interval in seconds
    :param total_duration: Total duration to record in seconds
    :param output_file_prefix: Prefix for the output mp3 files
    """
    intervals = total_duration // interval_duration
    for i in range(intervals):
        output_file = f"{output_file_prefix}_{i+1}.mp3"
        record_radio(url, interval_duration, output_file)
        print(f"Recording {i+1} saved to {output_file}")
        time.sleep(1)  # Ensure there's a small delay between recordings to avoid overlap

def record_radio_continuous(url, total_duration, temp_file):
    """
    Records online radio continuously for a specified duration and saves it as a raw file.
    
    :param url: URL of the online radio stream
    :param total_duration: Total duration to record in seconds
    :param temp_file: Path to the temporary raw file
    """
    response = requests.get(url, stream=True)

    with open(temp_file, "wb") as f:
        start_time = time.time()
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
            if time.time() - start_time > total_duration:
                break

def split_recording(temp_file, interval_duration, output_file_prefix):
    """
    Splits the continuous recording into intervals and saves them as mp3 files.
    
    :param temp_file: Path to the temporary raw file
    :param interval_duration: Duration of each recording interval in seconds
    :param output_file_prefix: Prefix for the output mp3 files
    """
    audio_segment = AudioSegment.from_file(temp_file, format="raw", frame_rate=44100, channels=2, sample_width=2)
    total_duration = len(audio_segment) // 1000  # Convert to seconds
    intervals = total_duration // interval_duration

    for i in range(intervals):
        start_time = i * interval_duration * 1000  # Convert to milliseconds
        end_time = start_time + interval_duration * 1000  # Convert to milliseconds
        interval_segment = audio_segment[start_time:end_time]
        output_file = f"{output_file_prefix}_{i+1}.mp3"
        interval_segment.export(output_file, format="mp3")
        print(f"Recording {i+1} saved to {output_file}")

def record_radio_with_backup(url, interval_duration, total_duration, temp_file_prefix, output_file_prefix):
    """
    Records online radio continuously with periodic backups and saves it as mp3 files.
    
    :param url: URL of the online radio stream
    :param interval_duration: Duration of each recording interval in seconds
    :param total_duration: Total duration to record in seconds
    :param temp_file_prefix: Prefix for the temporary raw files
    :param output_file_prefix: Prefix for the output mp3 files
    """
    response = requests.get(url, stream=True)
    total_intervals = total_duration // interval_duration

    for i in range(total_intervals):
        temp_file = f"{temp_file_prefix}_{i+1}.raw"
        with open(temp_file, "wb") as f:
            start_time = time.time()
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
                if time.time() - start_time > interval_duration:
                    break

        audio_segment = AudioSegment.from_file(temp_file, format="raw", frame_rate=44100, channels=2, sample_width=2)
        output_file = f"{output_file_prefix}_{i+1}.mp3"
        audio_segment.export(output_file, format="mp3")
        print(f"Recording {i+1} saved to {output_file}")
        os.remove(temp_file)

def shutdown_computer():
    """
    Shuts down the computer.
    """
    os.system("shutdown /s /t 1")

if __name__ == "__main__":
    radio_url = "https://stream.rcs.revma.com/asn0cmvb938uv"
    interval_duration = 900  # Record each interval for 15 minutes (900 seconds)
    total_duration = 9000  # Total duration to record is 2.5 hours (9000 seconds)
    temp_file_prefix = "temp_stream"
    output_file_prefix = "recorded_radio"
    
    record_radio_with_backup(radio_url, interval_duration, total_duration, temp_file_prefix, output_file_prefix)
    shutdown_computer()