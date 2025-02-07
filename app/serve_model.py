from flask import Flask, request, jsonify
import joblib
import numpy as np
import logging

app = Flask(__name__)

# Load your trained model
credit_model = joblib.load('../models/rf-credit.pkl')
fraud_model = joblib.load('../models/rf-fraud.pkl')

# Set up logging
logging.basicConfig(filename='fraud_detection.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

@app.route('/')
def home():
    return "Fraud Detection Model API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = np.array([data['features']])
        prediction = credit_model.predict(features)
        
        response = {'fraud_prediction': int(prediction[0])}
        logging.info(f"Received request: {data} | Prediction: {response}")
        
        return jsonify(response)

    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
