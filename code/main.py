from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the flask_cors module
import openai
from elevenlabs.simple import generate
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS

openai.api_key = ''  # Replace with your actual OpenAI API key

@app.route('/message', methods=['POST'])
def generate_city():
    try:
        user_message = request.json['message']
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Giovanni who is simulating a conversation with a user. Always greet the user with your name(Giovanni). Keep your responses short and human-like."},
                {"role": "user", "content": user_message}
            ]
        )
  
        city = response.choices[0].message.content

        # Generate audio from the generated text
        audio = generate(
            text=city,
            voice="Giovanni",  # Replace with the correct voice name
            model="eleven_turbo_v2"
        )

        # Convert the audio data to a base64 string
        audio_base64 = base64.b64encode(audio).decode('utf-8')

        # Return the generated text and audio
        return jsonify({'city': city, 'audio': audio_base64})

    except Exception as e:
        return jsonify({'error': 'Exception occurred', 'message': str(e)}), 500

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad request', 'message': str(e)}), 400

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)