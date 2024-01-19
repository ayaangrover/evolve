from flask import Flask, jsonify, Response, send_file
from flask_cors import CORS
import openai
from elevenlabs import generate, stream, set_api_key
import os

app = Flask(__name__)
CORS(app)

openai.api_key = ''
set_api_key("")

@app.route('/message', methods=['POST'])
def generate_city():
    user_message = request.json['message']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": user_message + " and also keep your response short, to simulate human conversation."}
        ]
    )
  
    city = response.choices[0].message.content

    def text_stream():
        yield city

    audio_stream = generate(
        text=text_stream(),
        voice="Nicole",
        model="eleven_monolingual_v1",
        stream=True
    )

    # Save the audio stream to a file
    with open('audio.wav', 'wb') as f:
        for chunk in audio_stream:
            f.write(chunk)

    # Return the text and the audio URL
    return jsonify({'text': city, 'audio_url': 'http://127.0.0.1:5000/audio'})

@app.route('/audio')
def audio():
    return send_file('audio.wav', mimetype='audio/wav')

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000)