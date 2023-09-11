from __future__ import annotations

import os
from pydub import AudioSegment


def create_audio_file_stub(audio_input_path: str, audio_output_path: str, second_length: int = 600) -> None:
    """
    Creates an audio file from the input path and exports it to the output path
    :param audio_input_path: The path to the audio file to be truncated
    :param audio_output_path: The path to the audio file to be created
    :param second_length: The length of the audio file in seconds
    """
    print("#" * 50)
    print("Creating Audio File")

    if not os.path.isfile(audio_output_path):
        print("New Audio File: truncating and writing to new file")
        audio_file = AudioSegment.from_file(audio_input_path)

        first_ten_min = audio_file[:(second_length / 60) * 60 * 1000]

        first_ten_min.export(audio_output_path, format="mp3")
        print("Exported truncated audio")
    else:
        print("Audio File already exists")

    print("#" * 50)


def create_audio_files(audio_input_path: str, audio_output_path: str, second_length: int = 600, second_offset: int = 0) -> list[str]:
    """
    Creates audio files from the input path and exports them to the output directory
    :param audio_input_path: The path to the audio file to be truncated
    :param audio_output_directory: The directory where the audio files will be created
    :param second_length: The length of each audio file segment in seconds (default is 600 seconds or 10 minutes)
    :param second_offset: The offset in seconds to start the first segment (default is 0 seconds)
    """
    print("#" * 50)
    print("Creating Audio Files")

    # Create a new directory to store the output files
    # audio_output_directory = os.path.join(os.path.dirname(audio_output_path), pod_name)
    # audio_output_directory = os.path.dirname(audio_output_path)
    os.makedirs(audio_output_path, exist_ok=True)

    # Check if the file size is less than 100 MB
    file_size_mb = os.path.getsize(audio_input_path) / (1024 * 1024)
    if file_size_mb > 100:
        print(f"The file size is {file_size_mb:.2f} MB, which exceeds the 100 MB limit. Aborting.")
        return []

    audio_file = AudioSegment.from_file(audio_input_path)

    # Calculate the total number of segments
    total_segments = int(len(audio_file) / (second_length * 1000))
    
    created_files: list[str] = []

    for i in range(total_segments + 1):
        start_ms = i * second_length * 1000 + second_offset * 1000
        end_ms = min(start_ms + second_length * 1000, len(audio_file) - 1)
        
        # Generate a filename for each segment
        output_path = os.path.join(audio_output_path, f"segment_{i+1}.mp3")

        if not os.path.isfile(output_path):
            print(f"Creating segment {i+1}: {start_ms//1000} to {end_ms//1000} seconds")
            segment = audio_file[start_ms:end_ms]
            segment.export(output_path, format="mp3")
            print(f"Exported segment {i+1}")
        else:
            print(f"Segment {i+1} already exists")
            
        created_files.append(output_path)

    print("#" * 50)
    
    return created_files