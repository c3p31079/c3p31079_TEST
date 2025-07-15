# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from crack_detector import detect_crack_length

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '✅ API is alive. POST to /analyze with image file.'

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    image_bytes = file.read()
    result = detect_crack_length(image_bytes)

    return jsonify(result)
