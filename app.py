# app.py
from flask import Flask, render_template, request, jsonify
import pytesseract
import cv2
import os
import traceback

app = Flask(__name__)

# Create the 'static/images' directory if it doesn't exist
if not os.path.exists('static/images'):
    os.makedirs('static/images')

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_text(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            text = extract_text(filename)
            return jsonify({'text': text})

    except Exception as e:
        traceback.print_exc()  # Print the traceback to the console
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)

