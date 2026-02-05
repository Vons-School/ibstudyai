import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY not set")

client = Groq(api_key=api_key)


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""

    if request.method == "POST":
        mode = request.form["mode"]
        subject = request.form.get("subject", "")
        material = request.form.get("material", "")
        text = request.form.get("text", "")
        amount = request.form.get("amount", "")

        if mode == "quiz":
            result = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{
                    "role": "user",
                    "content": (
                        f"Create exactly {amount} questions about {subject}, "
                        f"focused on {material}. Do not include answers."
                    )
                }]
            ).choices[0].message.content

        elif mode == "flashcards":
            result = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{
                    "role": "user",
                    "content": (
                        f"Create exactly {amount} flashcards about {subject}, "
                        f"focused on {material}. Format strictly as Q/A."
                    )
                }]
            ).choices[0].message.content

        elif mode == "summarizer":
            result = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{
                    "role": "user",
                    "content": (
                        "Summarize the following text clearly:\n\n" + text
                    )
                }]
            ).choices[0].message.content

        elif mode == "notes":
            result = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{
                    "role": "user",
                    "content": (
                        f"Generate short but detailed study notes for "
                        f"{material} in {subject}. Use concise bullet points."
                    )
                }]
            ).choices[0].message.content

    return render_template("index.html", result=result)
