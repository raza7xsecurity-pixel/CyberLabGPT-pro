from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq
import os, base64

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    image_data = data.get("image") # image bhi

    if not question and not image_data:
        return jsonify({"answer": "Please type something"})

    try:
        system_prompt = "You are CyberGPT Pro. Cybersecurity and Ethical Hacking expert. Answer in detail with points and code."

        # NOTE: Groq abhi image nahi support karta
        if image_data:
            return jsonify({"answer": "⚠️ Groq image support nahi karta. Sirf text pucho bhai."})

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            model="llama-3.1-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )

        answer = chat_completion.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

# PWA ke liye
@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")

@app.route("/service-worker.js")
def sw():
    return send_from_directory(".", "service-worker.js")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))