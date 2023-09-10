from __future__ import annotations

import os

def parse_and_check_audio_file(file_path: str) -> tuple[str | None, str | None, bool]:
    if not file_path or not os.path.isfile(file_path):
        print("Audio file not found")
        return None, None, False
    
    file_name_with_extension = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    allowed_extensions = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']
    allowed_file = file_extension.lower() in allowed_extensions

    return file_name, file_extension, allowed_file