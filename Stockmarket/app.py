from flask import Flask, render_template, request, jsonify
import numpy as np
import yfinance as yf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Path to saved LSTM model
MODEL_PATH = "D:\MLPROJECTS\MoneyVest\StockMarket\lstm_model.h5"

# Load the trained model
try:
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Function to fetch historical stock data
def fetch_historical_data(ticker, period="3mo", interval="1d"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            return None
        return hist["Close"].dropna().tolist()
    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {e}")
        return None

# Function to preprocess data (scaling)
def preprocess_data(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(np.array(data).reshape(-1, 1))
    return data_scaled, scaler

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.get_json()
        ticker = data.get("company", "").strip().upper()
        if not ticker:
            return jsonify({"error": "Please provide a company ticker symbol."}), 400

        # Fetch historical data
        stock_data = fetch_historical_data(ticker)
        if stock_data is None or len(stock_data) < 30:
            return jsonify({"error": f"Insufficient historical data for {ticker}."}), 400

        # Scale data and prepare for prediction
        stock_scaled, scaler = preprocess_data(stock_data)
        stock_scaled = np.array(stock_scaled).reshape(1, len(stock_scaled), 1)

        # Make prediction
        prediction = model.predict(stock_scaled)
        predicted_price = scaler.inverse_transform([[prediction[0][0]]])[0][0]
        last_price = stock_data[-1]
        growth_value = predicted_price - last_price
        trend = "increasing" if growth_value > 0 else "decreasing"

        return jsonify({
            "company": ticker,
            "predicted_price": round(predicted_price, 2),
            "last_price": round(last_price, 2),
            "growth": round(growth_value, 2),
            "trend": trend
        })

    except Exception as e:
        return jsonify({"error": f"Error making prediction: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)

