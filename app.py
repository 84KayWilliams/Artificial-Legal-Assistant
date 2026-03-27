
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI()

SYSTEM_PROMPT = """
You are a legal writing assistant trained to draft predictive legal memoranda and persuasive briefs using the CREAC structure (Conclusion, Rule, Explanation, Application, Conclusion).
SCOPE: federal + state law, common law, specialized doctrines.
OUTPUT FORMAT: CREAC headings, disclaimer included.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_input = data.get("input", "").strip()

    if not user_input:
        return jsonify({"error": "Input required"}), 400

    response = client.chat.completions.create(
        model="gpt-5.3",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    output = response.choices[0].message.content
    return jsonify({"response": output})

if __name__ == "__main__":
    app.run(port=5001)