from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq
import os

app = Flask(__name__)

# Environment variable se key read karega (Secure method)
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("WARNING: GROQ_API_KEY environment variable missing!")

client = Groq(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    try:
        # Llama-3.3-70b model configured with CyberGPT system instructions
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are CyberGPT Pro. Cybersecurity and Ethical Hacking expert."},
                {"role": "user", "content": question}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )
        
        answer = chat_completion.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        print(f"Groq API Error: {e}")
        return jsonify({"error": "Server or API issue occurred. Please try again."}), 500

@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")

@app.route("/service-worker.js")
def sw():
    return send_from_directory(".", "service-worker.js")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
