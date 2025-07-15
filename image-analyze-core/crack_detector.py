
import cv2
import numpy as np

def detect_crack_endpoints(image_bytes):
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    longest = max(contours, key=cv2.arcLength)
    epsilon = 0.01 * cv2.arcLength(longest, True)
    approx = cv2.approxPolyDP(longest, epsilon, True)

    if len(approx) >= 2:
        pt1 = tuple(approx[0][0])
        pt2 = tuple(approx[-1][0])
        return pt1, pt2
    return None
