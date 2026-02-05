import os
import json
from groq import Groq

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": "Method Not Allowed"
        }

    data = request.json()

    subject = data.get("subject", "")
    material = data.get("material", "")
    qamount = data.get("qamount", "5")
    qtype = data.get("qtype", "Choices")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = (
        f"You are a deterministic quiz generator. "
        f"Create exactly {qamount} questions about {subject}, "
        f"focused on {material}, using the question type {qtype}. "
        "Do NOT include answers, explanations, hints, emojis, or markdown. "
        "Number each question clearly. "
        "If Choices, use exactly 4 options labeled A–D. "
        "If True/False, ensure each question is unambiguous."
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "statusCode": 200,
        "headers": { "Content-Type": "text/plain" },
        "body": response.choices[0].message.content
    }
