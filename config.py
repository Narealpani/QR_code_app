import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")  # Folder containing nameplate files
QR_FOLDER = os.path.join(BASE_DIR, "static", "qr_codes")  # QR image output folder
HOST_IP = "0.0.0.0" 
#HOST_IP = "10.36.58.39" # Replace with your actual IP address
PORT = 5000
#app.run(host="0.0.0.0", port=5000, debug=True)


# Web-accessible base URL
BASE_URL = f"http://{HOST_IP}:{PORT}/files/"

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)
