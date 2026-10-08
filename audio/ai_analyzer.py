import os

from openai import OpenAI
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================
load_dotenv()
MODEL = "openrouter/free"


# ============================================================
# CLIENT
# ============================================================

def get_client():

    api_key = os.getenv(
        "OPENROUTER_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "OPENROUTER_API_KEY environment variable "
            "is missing."
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )


# ============================================================
# ANALYZE TRANSCRIPT
# ============================================================

def analyze_transcript(transcript):

    client = get_client()

    prompt = f"""
You are an AI meeting assistant.

Analyze the following meeting transcript.

Write a professional but natural meeting recap.

Use exactly these sections:

1. MEETING SUMMARY

Give a clear and human-readable summary of
what the meeting was mainly about.

2. KEY POINTS

List the most important topics discussed.

3. DECISIONS

List decisions that were actually made.

If there were no clear decisions, write:

None identified.

4. ACTION ITEMS

List the tasks that need to be completed.

Mention the responsible person only if
the transcript clearly identifies them.

Do not invent names or responsibilities.

5. IMPORTANT DETAILS

Mention useful information, deadlines,
dates, constraints or other details that
are worth remembering.

IMPORTANT RULES:

- Do not invent information.
- Only use information present in the transcript.
- Keep the writing natural and professional.
- Avoid unnecessary repetition.
- Make the recap easy to read.
- Use bullet points where appropriate.

MEETING TRANSCRIPT:

{transcript}
"""

    print(
        "🤖 Sending transcript to OpenRouter..."
    )

    response = client.chat.completions.create(
        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional AI meeting "
                    "assistant. Analyze meeting transcripts "
                    "accurately and never invent information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        stream=False
    )

    return response.choices[0].message.content