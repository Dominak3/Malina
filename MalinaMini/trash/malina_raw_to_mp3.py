from pydub import AudioSegment
import os
import re

# Set the path to ffmpeg and ffprobe
current_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(current_dir, 'ffmpeg')
AudioSegment.converter = ffmpeg_path
AudioSegment.ffprobe = os.path.join(current_dir, 'ffprobe')

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
        temp_file = os.path.join(folder_path, file_name)
        output_file = os.path.join(output_folder, file_name.replace(".raw", ".mp3"))
        audio_segment = AudioSegment.from_file(temp_file, format="raw", frame_rate=44100, channels=2, sample_width=2)
        audio_segment.export(output_file, format="mp3")
        print(f"Converted {temp_file} to {output_file}")

if __name__ == "__main__":
    folder_path = "C:/Users/dominak3/Desktop/radio/conv"  # Replace with the path to your folder containing raw files
    output_folder = "C:/Users/dominak3/Desktop/radio/"  # Replace with the path to your output folder
    
    convert_raw_files_in_folder(folder_path, output_folder)
