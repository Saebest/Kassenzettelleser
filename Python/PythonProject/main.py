from flask import Flask, request, jsonify,render_template
from PIL import Image
import io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    img = Image.open(io.BytesIO(file.read()))
    width, height = img.size
    return jsonify({"width": width, "height": height})

if __name__ == "__main__":
    app.run(debug=True, port=5000,host="0.0.0.0")