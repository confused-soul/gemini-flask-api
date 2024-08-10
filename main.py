from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import base64
import pathlib

# Configure the API key
my_secret = os.environ.get('API')
genai.configure(api_key=my_secret)

# Instantiate the model
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

def base64_to_image(base64_string, output_path):
    """Convert a base64 string to a JPG image and save it to the specified output path."""
    try:
        # Decode the base64 string to bytes
        image_data = base64.b64decode(base64_string)
        
        # Write the image data to a file
        with open(output_path, "wb") as image_file:
            image_file.write(image_data)
        
        print(f"Image saved as {output_path}")
    except Exception as e:
        print(f"Error: {e}")

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.get_json()

    if not data or 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400

    prompt = data['prompt']
    image_data = data.get('image')

    if image_data:
        try:
            # Usage example
            base64_string =  image_data # Replace with your base64 string
            output_path = 'output_image.jpg'  # Specify the output file path

            base64_to_image(base64_string, output_path)

        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 400

    # Generate content using the Gemini model
    try:
        
        image1 = {
            'mime_type': 'image/jpeg',
            'data': pathlib.Path('output_image.jpg').read_bytes()
        }
        response = model.generate_content([prompt, image1])
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': f'Error generating content: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
