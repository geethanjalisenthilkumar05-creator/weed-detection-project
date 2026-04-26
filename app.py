from flask import Flask, render_template, request
import os
from tensorflow.keras.models import load_model
import requests
import numpy as np
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
MODEL_PATH = "/tmp/weed_model.h5"

if not os.path.exists(MODEL_PATH):
    url = "https://drive.google.com/file/d/1APmmhRbiDlT4fPJgD4SU6yytPqUrIIl6/view?usp=sharing"
    r = requests.get(url)
    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)

model = load_model(MODEL_PATH)

UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    herbicide = ""

    if request.method == "POST":
        file = request.files.get("image")

        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            img = image.load_img(filepath, target_size=(150, 150))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0

prediction = model.predict(img_array)

if prediction[0][0] > 0.5:
    result = "Weed detected"
    herbicide = "Pendimethalin (0.3 - 0.4 ml)"
else:
    result = "Crop detected"
    herbicide = "No herbicide required"

    return render_template("index.html", result=result, herbicide=herbicide)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
