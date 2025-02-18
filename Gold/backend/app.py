from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import datetime
import pandas as pd

app = Flask(__name__)
model = load_model(r"D:\MLPROJECTS\MoneyVest\Gold\backend\model_lstm.h5")  # Load pre-trained LSTM model
scaler = MinMaxScaler(feature_range=(0, 1))

def predict_price(date):
    # Dummy function for predicting price, replace with actual logic
    future_price = np.random.uniform(1800, 2000)  # Random price for now
    last_price = 1900  # Example last known price
    movement = "Up" if future_price > last_price else "Down"
    return {"price": future_price, "movement": movement}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    date = data.get("date")
    if not date:
        return jsonify({"error": "No date provided"}), 400
    prediction = predict_price(date)
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True)
