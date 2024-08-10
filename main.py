from flask import Flask, request, jsonify
import google.generativeai as genai
import os

my_secret = os.environ.get('API')
# Configure the API key
genai.configure(api_key=my_secret)

# Instantiate the model
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.get_json()

    if 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400

    prompt = data['prompt']

    # Generate content using the Gemini model
    response = model.generate_content(prompt)

    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
