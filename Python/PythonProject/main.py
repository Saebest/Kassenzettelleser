from flask import Flask, request, jsonify,render_template
from PIL import Image
import io
from KassenzettelLeser import read_image

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/size", methods=["POST"])
def upload():
    print(request.files)
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    img = Image.open(io.BytesIO(file.read()))
    width, height = img.size
    return jsonify({"width": int(width), "height": int(height)})

if __name__ == "__main__":
    app.run(debug=True, port=5000,host="0.0.0.0")