# backend/crack_detector.py
import cv2
import numpy as np
import io
from PIL import Image

def detect_crack_length(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img_np = np.array(image)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # しきい値処理 → 輪郭検出
    _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return {"error": "No crack detected"}

    # 最大の輪郭を亀裂と見なす
    crack = max(contours, key=cv2.contourArea)
    leftmost = tuple(crack[crack[:, :, 0].argmin()][0])
    rightmost = tuple(crack[crack[:, :, 0].argmax()][0])
    topmost = tuple(crack[crack[:, :, 1].argmin()][0])
    bottommost = tuple(crack[crack[:, :, 1].argmax()][0])

    # 最長端点間の距離（ピクセル単位）
    endpoints = [leftmost, rightmost, topmost, bottommost]
    max_dist = 0
    point_a, point_b = leftmost, rightmost

    for i in range(len(endpoints)):
        for j in range(i+1, len(endpoints)):
            dist = np.linalg.norm(np.array(endpoints[i]) - np.array(endpoints[j]))
            if dist > max_dist:
                max_dist = dist
                point_a, point_b = endpoints[i], endpoints[j]

    return {
        "point_a": {"x": int(point_a[0]), "y": int(point_a[1])},
        "point_b": {"x": int(point_b[0]), "y": int(point_b[1])},
        "pixel_length": float(max_dist)
    }
