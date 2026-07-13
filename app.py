from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are CyberGPT Pro. Cybersecurity and Ethical Hacking expert."},
            {"role": "user", "content": question}
        ],
        model="llama-3.3-70b-versatile", # <-- YE NAYA MODEL HAI
        temperature=0.7,
        max_tokens=1024,
    )
    return jsonify({"answer": chat_completion.choices[0].message.content})

@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")

@app.route("/service-worker.js")
def sw():
    return send_from_directory(".", "service-worker.js")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))