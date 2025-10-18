from flask import Flask, request, jsonify,render_template
from PIL import Image
import io
from KassenzettelLeser import KassezettelLeser
from KassenzettelItem import *

app = Flask(__name__)
leser = KassezettelLeser()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/size", methods=["POST"])
def upload():
    print("Received File",request.files)
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    print(leser.reader)
    img = Image.open(io.BytesIO(file.read()))
    try:
        output = leser.read_image(img)
        json = output.to_json()
        print(json)
        return json
    except Exception:
        return jsonify({"error": "Unable to read image"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000,host="0.0.0.0")