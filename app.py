from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

# Load trained model
model = tf.keras.models.load_model("weed_model.h5")

# Classes
classes = ["crop", "weed"]

# Create uploads folder if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    herbicide = ""

    if request.method == "POST":

        file = request.files["image"]

        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        # Image preprocessing
        img = Image.open(filepath)
        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        # Prediction
        prediction = model.predict(img)

        class_name = classes[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        if class_name == "weed":
            result = "Weed detected"

            if confidence < 0.7:
                herbicide = "Recommended Herbicide: Pendimethalin 0.3-0.4 ml for this weed patch"
            else:
                herbicide = "Recommended Herbicide: Pendimethalin 0.5-0.6 ml for higher weed density"

        else:
            result = "Crop detected"
            herbicide = "No herbicide required"

    return render_template("index.html", result=result, herbicide=herbicide)


if __name__ == "__main__":
    app.run(debug=True)