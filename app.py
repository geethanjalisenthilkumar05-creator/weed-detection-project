 from flask import Flask, render_template, request
import os
from PIL import Image

app = Flask(__name__)

# Make sure uploads folder exists
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    herbicide = ""

    if request.method == "POST":
        file = request.files["image"]

        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # 🔴 DEMO RESULT (since model is removed for deployment)
            result = "Weed detected"
            herbicide = "Recommended Herbicide: Pendimethalin (0.3 - 0.4 ml)"

    return render_template("index.html", result=result, herbicide=herbicide)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
