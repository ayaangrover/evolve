from flask import Flask, jsonify
import openai
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)

openai.api_key = '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'

@app.route('/message', methods=['POST'])
def generate_city():
    user_message = request.json['message']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": user_message}
        ]
    )
  
    city = response.choices[0].message.content
    return jsonify({'city': city})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)