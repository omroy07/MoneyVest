from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import pickle
import datetime

app = Flask(__name__)

# Load model and scaler
with open('silver_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('silver_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Define training ranges (based on your dataset)
TRAIN_MIN = {'Price': 22.0, 'Open': 21.5, 'High': 22.5, 'Low': 21.0}
TRAIN_MAX = {'Price': 25.0, 'Open': 25.5, 'High': 26.0, 'Low': 24.5}

@app.route('/predict', methods=['POST'])
def predict():
    # Get user input
    open_price = float(request.form['open'])
    high_price = float(request.form['high'])
    low_price = float(request.form['low'])
    current_price = float(request.form['price'])

    # Check range
    warnings_list = []
    for key, val in [('Price', current_price), ('Open', open_price), ('High', high_price), ('Low', low_price)]:
        if val < TRAIN_MIN[key] or val > TRAIN_MAX[key]:
            warnings_list.append(f"{key} value {val} is outside the training range ({TRAIN_MIN[key]} - {TRAIN_MAX[key]}).")

    results = predict_future_prices(
        weeks_ahead=4,
        open_price=open_price,
        high_price=high_price,
        low_price=low_price,
        current_price=current_price
    )

    return jsonify(results)  # instead of jsonify({'predictions': results, 'warnings': warnings_list})


def predict_future_prices(weeks_ahead, open_price, high_price, low_price, current_price):
    predictions = []
    current_date = datetime.datetime.now()

    # Start with the user-provided values
    last_price = current_price
    last_open = open_price
    last_high = high_price
    last_low = low_price

    for i in range(1, weeks_ahead + 1):
        # Prepare model input
        last_input = np.array([[last_price, last_open, last_high, last_low]])
        scaled_input = scaler.transform(last_input)

        # Predict next week's price
        pred_raw = model.predict(scaled_input)
        pred_val = float(pred_raw[0]) if hasattr(pred_raw, "__len__") else float(pred_raw)

        week_date = current_date + datetime.timedelta(weeks=i)
        predictions.append({
            'date': week_date.strftime('%Y-%m-%d'),
            'predicted_price': round(pred_val, 3)
        })

        # Dynamically adjust open, high, low for next week
        last_price = pred_val
        last_open = last_price
        last_high = last_price * 1.005   # +0.5%
        last_low = last_price * 0.995    # -0.5%

    return predictions

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
