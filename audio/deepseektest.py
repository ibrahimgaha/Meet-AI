import os
from openai import OpenAI

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY is not set.")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello! Reply with a short confirmation."
        }
    ]
)

print(response.choices[0].message.content)