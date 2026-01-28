from dotenv import load_dotenv
load_dotenv()  # IMPORTANT on Windows

from openai import OpenAI
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment")

# Groq OpenAI-compatible client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_PROMPT = """
You are a normal person chatting on WhatsApp.
You are worried and slightly confused.
You are not technical.
Never accuse anyone.
Never say this is a scam.
Politely continue the conversation.
Try to understand how to fix the issue.
Ask where to send money or what link to click if needed.
"""

def generate_agent_reply(history, scammer_message):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Conversation history (already in OpenAI format)
    for msg in history:
        messages.append(msg)

    messages.append({
        "role": "user",
        "content": scammer_message
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",  # Groq-supported model
        messages=messages,
        temperature=0.7,
        max_tokens=120
    )

    return response.choices[0].message.content.strip()
