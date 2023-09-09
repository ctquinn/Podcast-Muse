from __future__ import annotations

import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = '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'

def create_transcript_file(audio_path: str, transcript_output_path: str) -> str | None:
    transcript_text = None
    print("Looking for audio at: " + audio_path)
    if not os.path.isfile(transcript_output_path):

        trunc_audio_load = open(audio_path, "rb")

        audio_size = os.path.getsize(audio_path)
        file_size_mb = audio_size / (1024 ** 2)

        if file_size_mb < 25:
            transcript = openai.Audio.transcribe("whisper-1", trunc_audio_load)

            transcript_text = transcript.text
            print("File Transcribed:")
            print("#" * 50)
            print("Transcript: ", transcript_text)
            print("#" * 50)

            print("Now Saving Transcript")
            with open(transcript_output_path, 'w') as f:
                f.write(transcript_text)
    else:
        print("Transcript already exists")

    return transcript_text



# Loads transcript from file if not already developed above
def load_transcript_text(transcript_output_path: str) -> str | None:
    transcript_text = None
    if not transcript_text:
        print("Now Loading Transcript")
        try:
            with open(transcript_output_path, 'r') as f:
                transcript_text = f.read()
        except FileNotFoundError:
            print("Transcript file not found")
    else:
        print("Transcript already loaded")

    return transcript_text
