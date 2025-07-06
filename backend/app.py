from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  #全ルートがCORS許可される

@app.route('/')
def index():
    return '✅ API is alive. POST to /analyze with image file.'

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    from PIL import Image
    import io

    image = Image.open(file.stream)
    width, height = image.size

    return jsonify({'width': width, 'height': height})
