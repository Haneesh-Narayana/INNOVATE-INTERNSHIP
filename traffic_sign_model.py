import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

def load_traffic_sign_model(model_path):
    # Load the pre-trained model
    model = load_model(model_path)
    return model

def preprocess_image(img_path):
    # Load the image and resize it to the target size
    img = image.load_img(img_path, target_size=(32, 32))
    # Convert the image to a numpy array
    img_array = image.img_to_array(img)
    # Expand dimensions to match the model input
    img_array = np.expand_dims(img_array, axis=0)
    # Normalize the image
    img_array /= 255.0
    return img_array

def predict_traffic_sign(model, img_path):
    # Preprocess the image
    processed_img = preprocess_image(img_path)
    # Get the prediction from the model
    prediction = model.predict(processed_img)
    # Get the class with the highest probability
    predicted_class = np.argmax(prediction, axis=1)[0]
    return predicted_class
