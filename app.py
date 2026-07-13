from flask import Flask, render_template, request, jsonify
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
    question = data["question"]
    
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"You are CyberLabGPT Pro, a cybersecurity AI assistant. Be helpful and accurate. Question: {question}"
        }],
        model="llama-3.1-8b-instant", # ye wala model abhi working hai
        temperature=0.7
    )
    
    return jsonify({"answer": chat_completion.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)