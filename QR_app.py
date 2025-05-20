from flask import Flask, send_from_directory, abort, render_template_string, request, redirect, url_for, flash
import os
from config import UPLOAD_FOLDER, QR_FOLDER
import qrcode

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flashing messages

ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}

# Utility to check allowed file types
def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

# Generate QR Code after upload
def generate_qr_for_file(filename):
    file_url = f"http://{request.host}/files/{filename}"
    qr = qrcode.make(file_url)
    qr_path = os.path.join(QR_FOLDER, f"{filename}.png")
    qr.save(qr_path)

# Homepage: List uploaded files with QR
@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    files = [f for f in files if allowed_file(f)]
    html = """
    <h2>📄 Equipment Nameplate Files</h2>
    <a href="/upload">⬆️ Upload New File</a>
    <ul>
    {% for file in files %}
        <li>
            {{ file }} <br>
            <a href="/files/{{ file }}">🔗 View File</a> |
            <a href="/qrs/{{ file }}.png">🧷 QR Code</a><br>
            <img src="/qrs/{{ file }}.png" width="120">
        </li><br>
    {% endfor %}
    </ul>
    """
    return render_template_string(html, files=files)

# Upload Page
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('⚠️ No file part in the request.')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('⚠️ No file selected.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            save_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(save_path)
            generate_qr_for_file(file.filename)
            flash('✅ File uploaded and QR code generated!')
            return redirect(url_for('index'))
        else:
            flash('❌ File type not allowed.')
            return redirect(request.url)

    html = """
    <h2>⬆️ Upload Equipment Nameplate File</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <input type="submit" value="Upload">
    </form>
    <a href="/">⬅️ Back to Home</a>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color: green;">
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    """
    return render_template_string(html)

# Serve uploaded files
@app.route('/files/<path:filename>')
def serve_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        abort(404)

# Serve QR codes
@app.route('/qrs/<path:filename>')
def serve_qr(filename):
    try:
        return send_from_directory(QR_FOLDER, filename)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
