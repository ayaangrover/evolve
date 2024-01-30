from flask_cors import CORS
from flask import Flask, request, jsonify, send_file
from elevenlabs.simple import generate
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = ''  # replace with your OpenAI API key

# This will act as our "memory"
memory = []

@app.route('/message', methods=['POST'])
def generate_city():
    user_message = request.json['message']

    # Add the user's message to the memory
    memory.append({"role": "user", "content": user_message})

    # Generate a list of messages for the chat model, starting with the system message
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ] + memory

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Add the AI's response to the memory
    ai_message = response.choices[0].message.content
    memory.append({"role": "assistant", "content": ai_message})

    # Generate voice from the AI's response
    voice_response = generate(
        model="eleven_turbo_v2",
        voice="Giovanni",
        text=ai_message  # replace with your ElevenLabs API key
    )

    # Save the voice response to a file
    filename = 'voice_response.wav'
    with open(filename, 'wb') as f:
        f.write(voice_response)

    return jsonify({'city': ai_message, 'audio': filename})

@app.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    return send_file(filename, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)