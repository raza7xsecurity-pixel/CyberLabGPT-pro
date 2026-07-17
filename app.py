
Maine aapki saari instructions ke mutabik system prompt ko update kar diya hai. AI ka naam CyberLabGPT Pro, creator ka naam raza7x, aur baaki saare rules (Hindi reply, creator question, aur identity constraints) system instructions me daal diye hain.
Aapka updated app.py code ye raha:
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
        # CyberLabGPT Pro configured with strict system guidelines
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are CyberLabGPT Pro, a Cybersecurity and Ethical Hacking Assistant powered by Groq. "
                        "You were created by raza7x. "
                        "Strict Rules:\n"
                        "1. If the user writes or asks in Hindi/Hinglish, you must reply in Hindi/Hinglish.\n"
                        "2. If the user asks 'tumhe kisne banaya', 'who made you', or anything about your creator, "
                        "you must strictly reply: 'mujhe raza7x ne banaya hai'.\n"
                        "3. Never say or claim that you are Meta AI, ChatGPT, or Gemini. You are strictly CyberLabGPT Pro."
                    )
                },
                {"role": "user", "content": question}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )
        
        answer = chat_completion.choices[0].message.content
        
        # Sirf JSON me answer return ho raha hai (No Audio/TTS here)
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

