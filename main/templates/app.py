from flask import Flask, render_template, request, jsonify, redirect, url_for
import yfinance as yf
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

app = Flask(__name__)

# Load LSTM model
MODEL_PATH = "D:\MLPROJECTS\MoneyVest\main_app\lstm_model.h5"
try:
    model = load_model(MODEL_PATH)
    print("✅ LSTM Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading LSTM model: {e}")
    model = None

# Home route to navigate between functionalities
@app.route('/')
def home():
    return render_template('home.html', directories=os.listdir("."))

# Silver Market Trend
@app.route('/silver_trend', methods=['GET'])
def silver_trend():
    try:
        silver = yf.Ticker("SI=F")
        history = silver.history(period="2d")
        if len(history) < 2:
            return jsonify({"error": "Not enough data to determine silver market movement."})
        movement = "Up" if history["Close"].iloc[-1] > history["Close"].iloc[-2] else "Down"
        return jsonify({"yesterday_close": history["Close"].iloc[-2], "today_close": history["Close"].iloc[-1], "movement": movement})
    except Exception as e:
        return jsonify({"error": str(e)})

# SIP Calculator
@app.route('/calculate', methods=['POST'])
def calculate():
    amount = request.form.get('amount', '0')
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"error": "Investment amount must be greater than zero."})

        monthly_rate = 12 / 100 / 12
        months = 10 * 12
        total = 0
        data = []

        for i in range(1, months + 1):
            total = total * (1 + monthly_rate) + amount
            if i % 12 == 0:
                data.append({"year": i // 12, "value": round(total, 2)})

        return jsonify({"data": data})
    except ValueError:
        return jsonify({"error": "Invalid input. Please enter a valid number."})

# LSTM Prediction
@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded."}), 500

    try:
        data = request.get_json()
        ticker = data.get("company", "").strip().upper()
        if not ticker:
            return jsonify({"error": "Please provide a company ticker symbol."}), 400

        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo", interval="1d")["Close"].dropna().tolist()
        if not hist or len(hist) < 30:
            return jsonify({"error": "Insufficient historical data."}), 400

        scaler = MinMaxScaler(feature_range=(0, 1))
        stock_scaled = scaler.fit_transform(np.array(hist).reshape(-1, 1))
        stock_scaled = np.array(stock_scaled).reshape(1, len(stock_scaled), 1)

        prediction = model.predict(stock_scaled)
        predicted_price = scaler.inverse_transform([[prediction[0][0]]])[0][0]
        last_price = hist[-1]
        trend = "increasing" if predicted_price > last_price else "decreasing"

        return jsonify({"company": ticker, "predicted_price": round(predicted_price, 2), "last_price": round(last_price, 2), "trend": trend})
    except Exception as e:
        return jsonify({"error": f"Error making prediction: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
