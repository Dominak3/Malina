from pydub import AudioSegment
import os
import re

def combine_mp3_files(input_folder, output_file):
    combined = AudioSegment.empty()
    
    mp3_files = [f for f in os.listdir(input_folder) if f.endswith('.mp3')]
    mp3_files.sort(key=lambda f: int(re.search(r'\d+', f).group()))

    for file_name in mp3_files:
        file_path = os.path.join(input_folder, file_name)
        audio = AudioSegment.from_mp3(file_path)
        combined += audio
    
    combined.export(output_file, format='mp3')

if __name__ == "__main__":
    input_folder = 'mp3'  # Replace with the path to your folder containing mp3 files
    output_file = 'combined_output.mp3'  # Replace with the desired output file path
    combine_mp3_files(input_folder, output_file)
    print(f"Combined MP3 files from '{input_folder}' into '{output_file}'")