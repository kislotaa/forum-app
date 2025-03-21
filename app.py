import openai
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Flask API is running!", 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Error: No message received"}), 400
        
        user_message = data["message"]
        print("User message:", user_message)  # Debugging

        # OpenAI API call using GPT-4o model
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("Error in /chat:", str(e))  # Print full error
        return jsonify({"reply": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port from environment variable
    app.run(host="0.0.0.0", port=port, debug=True)
