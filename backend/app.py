from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    height, width = img.shape[:2]
    return jsonify({'width': width, 'height': height})

@app.route('/')
def home():
    return '✅ API is alive. POST to /analyze with image file.'

if __name__ == '__main__':
    app.run(debug=True)
