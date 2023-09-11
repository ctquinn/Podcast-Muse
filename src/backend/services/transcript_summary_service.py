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
    """
    Uses GPT-3 to generate a five bullet summary from the input content
    :param content: The content to be summarized
    :return: The summary text (if generated)
    """
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
    """
    Generates a five bullet summary from the transcript text and exports it to the output path
    :param transcript_text: The transcript text to be summarized
    :param summary_output_path: The path to the summary file to be created
    :return: The summary text (if generated)
    """
    print("Now Summarizing")
    transcript_summary_text = None
    all_tokens = transcript_text.split()
    first_2000_tokens = all_tokens[:2000]
    resulting_tokens = ' '.join(first_2000_tokens)

    if not os.path.isfile(summary_output_path):
        transcript_summary = generate_five_bullet_audio_summary(resulting_tokens)
        transcript_summary_text = transcript_summary['choices'][0]['message']['content']
        
        # print(transcript_summ_tester)
        print("Now Saving Summary")
        summary_output_final_path = os.path.join(summary_output_path, "bullet_summary.txt")
        with open(summary_output_final_path, 'w') as f:
            f.write(transcript_summary_text)
        print("Done with 5 Bullet Summary")
    else:
        print("Summary already exists")
        with open(summary_output_path, 'r') as f:
            transcript_summary_text = f.read()
    
    return transcript_summary_text


def generate_answer_general_query(content: str, query: str) -> str:
    """
    Uses GPT-3 to generate an answer to the input query from the input content
    :param content: The content supplied to the model to answer the query
    :param query: The query to be answered
    :return: The answer text (if generated)
    """
    len_content = len(content)
    content_len_to_grab = min(len_content, 10000)

    all_tokens = content.split()
    first_2000_tokens = all_tokens[:2000]
    resulting_tokens = ' '.join(first_2000_tokens)

    # trimmed_content = content[:len_content]
    completion_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an expert in answering questions about the following text: {resulting_tokens}"},
            {"role": "user", "content": f': "Answer the following in 100 words or less: "{query}"'},
        ]
    )

    completion_response_text = completion_response['choices'][0]['message']['content']
    # formatted_response = '\n'.join([completion_response_text[i:i+50] for i in range(0, len(completion_response_text), 50)])
    formatted_words = completion_response_text.split()
    chunks = [' '.join(formatted_words[i:i+12]) for i in range(0, len(formatted_words), 12)]
    formatted_response = '\n'.join(chunks)

    return formatted_response