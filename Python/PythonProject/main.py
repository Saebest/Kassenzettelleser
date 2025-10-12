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
    print("Recieved File",request.files)
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    print(leser.reader)
    img = Image.open(io.BytesIO(file.read()))
    output = leser.read_image(img)

    print(output)
    width, height = img.size
    return jsonify({"width": int(width), "height": int(height),"menge": int(len(output.items))})

if __name__ == "__main__":
    app.run(debug=True, port=5000,host="0.0.0.0")