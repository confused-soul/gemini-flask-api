from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import base64
from PIL import Image
from io import BytesIO

# Configure the API key
my_secret = os.environ.get('API')
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
    image_base64 = data.get('image')

    # Prepare input for the model
    inputs = [prompt]

    if image_base64:
        try:
            # Decode the base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
            
            # Process image (e.g., convert to bytes or use directly)
            image_bytes = BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            
            # Add image bytes to the inputs
            inputs.append(image_bytes.getvalue())
            
        except Exception as e:
            return jsonify({'error': f'Error decoding image: {str(e)}'}), 400

    # Generate content using the Gemini model
    try:
        response = model.generate_content(inputs)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': f'Error generating content: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
