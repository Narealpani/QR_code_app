import streamlit as st
import qrcode
import os
from PIL import Image
from io import BytesIO

UPLOAD_FOLDER = "uploads"
QR_FOLDER = "static/qr_codes"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def generate_qr(file_url, filename):
    qr = qrcode.make(file_url)
    qr_path = os.path.join(QR_FOLDER, f"{filename}.png")
    qr.save(qr_path)
    return qr_path

st.title("📄 QR Code Generator for Equipment Files")

# Upload Section
st.header("⬆️ Upload File")
uploaded_file = st.file_uploader("Choose a PDF or Image", type=["pdf", "jpg", "jpeg", "png"])
if uploaded_file:
    filename = uploaded_file.name
    if allowed_file(filename):
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        file_url = f"your url/{filename}"  
        qr_path = generate_qr(file_url, filename)

        st.success("✅ File uploaded and QR code generated.")
        st.image(qr_path, caption="QR Code", width=200)
        st.markdown(f"[🔗 View File (placeholder)]({file_url})")
        st.markdown(f"[🧷 QR Image]({qr_path})")
    else:
        st.error("❌ File type not allowed.")

# List all files
st.header("📂 Uploaded Files and QR Codes")
files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
if not files:
    st.info("No files uploaded yet.")
else:
    for file in files:
        qr_image_path = os.path.join(QR_FOLDER, f"{file}.png")
        if os.path.exists(qr_image_path):
            st.markdown(f"**{file}**")
            st.image(qr_image_path, width=120)
