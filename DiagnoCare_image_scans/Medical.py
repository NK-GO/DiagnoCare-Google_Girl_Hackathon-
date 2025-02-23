from flask import Flask, render_template, request
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the trained model
model = load_model(r"C:\Users\yuwin\OneDrive\Desktop\medical image diagnosis\Medical image classification\medical_image_classifier.h5")  # Replace with your model file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        
        img = image.load_img(file_path, target_size=(250,250))  # Ensure to match the input size for the model
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.  # Normalize the image

        predictions = model.predict(img_array)
        class_names = [
            'Arthritis', 'Atherosclerosis', 'Bone Diseases, Metabolic', 'Bullous Emphysema',
            'Calcified Granuloma', 'Calcinosis', 'Emphysema', 'Fractures, Bone', 'Granuloma',
            'Granulomatous Disease', 'Hydropneumothorax', 'Hyperostosis, Diffuse Idiopathic Skeletal',
            'Hypovolemia', 'Kyphosis', 'Lung Diseases, Interstitial', 'Lung, Hyperlucent',
            'normal', 'Pneumonia', 'Pneumoperitoneum', 'Pneumothorax', 'Pulmonary Atelectasis',
            'Pulmonary Congestion', 'Pulmonary Disease, Chronic Obstructive', 'Pulmonary Edema',
            'Pulmonary Emphysema', 'Pulmonary Fibrosis', 'Sclerosis', 'Scoliosis', 'Spondylosis',
            'Thickening'
        ]  # Replace with your class names

        predicted_class = np.argmax(predictions)
        predicted_label = class_names[predicted_class]

        return render_template('result.html', predicted_label=predicted_label, file_path=file_path)

if __name__ == '__main__':
    app.run(debug=True)
