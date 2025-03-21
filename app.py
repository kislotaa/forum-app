import openai
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Error: No message received"}), 400
        
        user_message = data["message"]
        print("User message:", user_message)  # Debugging

        # Correct OpenAI API call using the new format
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        print("OpenAI response:", response)  # Debugging

        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("Error in /chat:", str(e))  # Print full error
        return jsonify({"reply": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
