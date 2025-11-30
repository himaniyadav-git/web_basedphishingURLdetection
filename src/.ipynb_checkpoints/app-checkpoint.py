# src/app.py
from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os
from tensorflow.keras.models import load_model
from features import extract_features_from_url

app = Flask(__name__, template_folder='../templates')

# Paths to model and scaler
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'phishing_model.h5')
SCALER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'scaler.pkl')

# Load model
print("Loading model from:", MODEL_PATH)
model = load_model(MODEL_PATH)
print("Model loaded.")

# Load scaler
scaler = joblib.load(SCALER_PATH)
print("Scaler loaded.")

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    url = ""
    if request.method == 'POST':
        url = request.form.get('url_input','').strip()
        if url:
            feats = extract_features_from_url(url).reshape(1, -1)
            feats_scaled = scaler.transform(feats)
            prob = float(model.predict(feats_scaled)[0][0])
            label = 'Phishing' if prob > 0.5 else 'Safe'
            result = {'label': label, 'score': round(prob,4)}
    return render_template('index.html', result=result, url=url)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json(force=True)
    url = data.get('url','')
    feats = extract_features_from_url(url).reshape(1,-1)
    feats_scaled = scaler.transform(feats)
    prob = float(model.predict(feats_scaled)[0][0])
    label = 'Phishing' if prob > 0.5 else 'Safe'
    return jsonify({'label': label, 'score': prob})

if __name__ == '__main__':
    app.run(debug=True)
