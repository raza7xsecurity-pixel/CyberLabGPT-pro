from flask import Flask, render_template, request, jsonify
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
    question = data["question"]
    image_data = data.get("image") # image bhi aayegi ab
    
    messages = [{"role": "user", "content": question}]
    
    # agar image bheji hai to usko bhi add kar denge
    if image_data:
        messages[0]["content"] = [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": image_data}}
        ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=1024
    )
    
    return jsonify({"answer": chat_completion.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)