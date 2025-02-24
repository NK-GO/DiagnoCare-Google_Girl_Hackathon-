from flask import Flask, render_template, request
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

app = Flask(__name__)

model_path = r"C:\Users\samri\OneDrive\Desktop\sammi_project\DiagnoCare_image_scans\Medical.py"
model = load_model(model_path)

class_labels = [
    'Arthritis', 'Atherosclerosis', 'Bone Diseases, Metabolic', 'Bullous Emphysema',
    'Calcified Granuloma', 'Calcinosis', 'Emphysema', 'Fractures, Bone', 'Granuloma',
    'Granulomatous Disease', 'Hydropneumothorax', 'Hyperostosis, Diffuse Idiopathic Skeletal',
    'Hypovolemia', 'Kyphosis', 'Lung Diseases, Interstitial', 'Lung, Hyperlucent',
    'Normal', 'Pneumonia', 'Pneumoperitoneum', 'Pneumothorax', 'Pulmonary Atelectasis',
    'Pulmonary Congestion', 'Pulmonary Disease, Chronic Obstructive', 'Pulmonary Edema',
    'Pulmonary Emphysema', 'Pulmonary Fibrosis', 'Sclerosis', 'Scoliosis', 'Spondylosis',
    'Thickening'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def make_prediction():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)

        img = image.load_img(file_path, target_size=(250, 250))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.

        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions)
        predicted_label = class_labels[predicted_class_index]

        return render_template('result.html', predicted_label=predicted_label, file_path=file_path)

if __name__ == '__main__':
    app.run(debug=True)
