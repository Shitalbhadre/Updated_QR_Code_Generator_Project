# Optional: Webcam scanning (skip if pyzbar issues)
from pyzbar.pyzbar import decode
from PIL import Image

def scan_qr(image_path):
    img = Image.open(image_path)
    data = decode(img)
    return data[0].data.decode("utf-8") if data else None
