from flask import Flask, jsonify
import pandas as pd
from datetime import datetime
import os, sys

# Initialize Flask app
app = Flask(__name__)

os.getcwd()
rpath = os.path.abspath('../')
if rpath not in sys.path:
    sys.path.insert(0,rpath)

# Construct the file path
file_path = os.path.join(rpath, 'data', 'merged_data.csv')

# Read the CSV file into a DataFrame
fraud_data = pd.read_csv(file_path)

# fraud_data.head()
# Load data
# fraud_data = pd.read_csv('Fraud_Data.csv')  # Update with your CSV path

# Preprocess the data
fraud_data['purchase_time'] = pd.to_datetime(fraud_data['purchase_time'])

@app.route('/summary', methods=['GET'])
def summary():
    # Define sample statistics with explicit conversions
    total_transactions = int(pd.Series([123456789])[0])  # Ensure it's a native int
    fraud_cases = int(pd.Series([9876])[0])  # Ensure it's a native int
    fraud_percentage = float(fraud_cases / total_transactions * 100)  # Convert to native float

    return jsonify({
        "total_transactions": total_transactions,
        "fraud_cases": fraud_cases,
        "fraud_percentage": fraud_percentage
    })

@app.route('/fraud_trends', methods=['GET'])
def fraud_trends():
    trends = fraud_data.set_index('purchase_time').resample('M')['class'].sum().reset_index()
    trends['purchase_time'] = trends['purchase_time'].dt.strftime('%Y-%m')
    return jsonify(trends.to_dict(orient="records"))

@app.route('/fraud_by_location', methods=['GET'])
def fraud_by_location():
    locations = fraud_data.groupby('country')['class'].sum().reset_index()
    return jsonify(locations.to_dict(orient="records"))

@app.route('/fraud_by_device_browser', methods=['GET'])
def fraud_by_device_browser():
    device_browser = fraud_data.groupby(['device_id', 'browser'])['class'].sum().reset_index()
    return jsonify(device_browser.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
