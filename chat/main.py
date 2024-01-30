from flask_cors import CORS
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = ''

# This will act as our "memory"
memory = []

@app.route('/message', methods=['POST'])
def generate_city():
    user_message = request.json['message']

    # Add the user's message to the memory
    memory.append({"role": "user", "content": user_message})

    # Generate a list of messages for the chat model, starting with the system message
    messages = [
        {"role": "system", "content": "You are a helpful assistant named Giovanni. You are not an AI."},
    ] + memory

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Add the AI's response to the memory
    memory.append({"role": "assistant", "content": response.choices[0].message.content})

    return jsonify({'city': response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)