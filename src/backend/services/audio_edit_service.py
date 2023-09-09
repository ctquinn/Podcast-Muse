from __future__ import annotations

import os
from pydub import AudioSegment


def create_audio_file(audio_input_path: str, audio_output_path: str, second_length: int = 600) -> None:
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
