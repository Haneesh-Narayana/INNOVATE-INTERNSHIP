import os
import csv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from traffic_sign_model import load_traffic_sign_model, preprocess_image

app = Flask(__name__)
CORS(app)

# Load the CSV file containing class names
def load_class_names(csv_file):
    class_names = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            class_id = int(row['ClassId'])
            class_names[class_id] = row['Name']
    return class_names

# Load the model
model_path = 'C:\\Users\\hanee\\OneDrive\\Desktop\\Traffic\\New folder\\model\\traffic_sign_model1.h5'
model = load_traffic_sign_model(model_path)

# Load the class names mapping
class_names = load_class_names('C:\\Users\\hanee\\OneDrive\\Desktop\\Traffic\\New folder\\labels.csv')

# Ensure the temporary directory exists
if not os.path.exists('temp'):
    os.makedirs('temp')

# Function to predict traffic sign label
def predict_traffic_sign_label(img_path):
    # Preprocess the image
    processed_img = preprocess_image(img_path)
    # Get the prediction from the model
    prediction = model.predict(processed_img)
    # Get the class with the highest probability
    predicted_class = int(prediction.argmax(axis=-1)[0])
    # Get the corresponding class name from the class names mapping
    predicted_name = class_names.get(predicted_class, 'Unknown')
    return predicted_name

# Route for rendering the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling image upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save file temporarily
    file_path = os.path.join('temp', file.filename)
    file.save(file_path)

    # Predict traffic sign label
    result = predict_traffic_sign_label(file_path)

    # Clean up the saved file
    os.remove(file_path)

    return jsonify({"output": result})

if __name__ == '__main__':
    app.run(debug=True)
