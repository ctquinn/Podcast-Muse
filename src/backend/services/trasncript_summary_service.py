from __future__ import annotations

import openai
import os

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


def generate_five_bullet_summary_text(transcript_text: str, summary_output_path: str) -> None:
    print("Now Summarizing")
    transcript_summary = generate_audio_summary(transcript_text)
    transcript_summ_tester = transcript_summary['choices'][0]['message']['content']
    
    # print(transcript_summ_tester)
    print("Now Saving Summary")
    summary_output_path_full = os.join(summary_output_path, "pod_summary.txt")
    with open(summary_output_path, 'w') as f:
        f.write(transcript_summ_tester)
    print("Done")