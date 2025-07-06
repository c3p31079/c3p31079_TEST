from flask import Flask, request, jsonify
import cv2
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '✅ API is alive. POST to /analyze with image file.'

@app.route('/analyze', methods=['POST'])
def analyze():
    # 画像処理コードなど
    file = request.files.get('image')
    if file:
        # 例：サイズを返すだけ
        from PIL import Image
        import io
        image = Image.open(file.stream)
        width, height = image.size
        return jsonify({'width': width, 'height': height})
    else:
        return jsonify({'error': 'No file provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
