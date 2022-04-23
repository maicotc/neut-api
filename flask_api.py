import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request
from flask_cors import CORS
import numpy as np
import flasgger
from flasgger import Swagger
from PIL import Image
import cv2
import json
import logging


app = Flask(__name__)
CORS(app)
Swagger(app)

model = load_model("neut_classifier.h5")


@app.route('/')
def welcome():
    return "Modifique URL para .../apidocs"


@app.route('/predict_image', methods=["POST"])
def PredictImage():
    """Return a classification for the given neutrophil image
    ---
    parameters:
        - name: image
          in: formData
          type: file
          required: true

    responses:
        200:
            description: successful operation

    """
    neut_image = Image.open(request.files['image'])
    img_array = np.array(neut_image)
    img_array = cv2.resize(img_array, (299, 299))
    img_array = cv2.cvtColor(np.array(img_array), cv2.COLOR_BGR2RGB)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)

    return json.dumps({
        "message": "percentage of Neutrophil classification",
        "data": {
            "N1": str(prediction[0][0]),
            "N2": str(prediction[0][1])
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
