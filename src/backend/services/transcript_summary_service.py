from __future__ import annotations

import openai
import os
from dotenv import load_dotenv
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

def generate_five_bullet_audio_summary(content: str) -> str:
    len_content = len(content)
    content_len_to_grab = min(len_content, 10000)

    trimmed_content = content[:len_content]
    completion_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You summarize texts in 5 bullet points or less."},
            {"role": "user", "content": f': "Summarize the following text in exactly 5 bullet points and in 200 words or less: "{trimmed_content}"'},
        ]
    )

    return completion_response


def generate_five_bullet_summary_text(transcript_text: str, summary_output_path: str) -> str:
    print("Now Summarizing")
    transcript_summary_text = None
    if not os.path.isfile(summary_output_path):
        transcript_summary = generate_five_bullet_audio_summary(transcript_text)
        transcript_summary_text = transcript_summary['choices'][0]['message']['content']
        
        # print(transcript_summ_tester)
        print("Now Saving Summary")
        with open(summary_output_path, 'w') as f:
            f.write(transcript_summary_text)
        print("Done with 5 Bullet Summary")
    else:
        print("Summary already exists")
        with open(summary_output_path, 'r') as f:
            transcript_summary_text = f.read()
    
    return transcript_summary_text


def generate_answer_general_query(content: str, query: str) -> str:
    len_content = len(content)
    content_len_to_grab = min(len_content, 10000)

    trimmed_content = content[:len_content]
    completion_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an expert in answering questions about the following text: {trimmed_content}"},
            {"role": "user", "content": f': "Answer the following in 100 words or less: "{query}"'},
        ]
    )

    completion_response_text = completion_response['choices'][0]['message']['content']
    # formatted_response = '\n'.join([completion_response_text[i:i+50] for i in range(0, len(completion_response_text), 50)])
    formatted_words = completion_response_text.split()
    chunks = [' '.join(formatted_words[i:i+12]) for i in range(0, len(formatted_words), 12)]
    formatted_response = '\n'.join(chunks)

    return formatted_response