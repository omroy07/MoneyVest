from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import datetime

app = Flask(__name__)

# Load model & scaler
with open('gold_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('gold_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def predict_future_prices(weeks_ahead, price, open_price, high_price, low_price, volume, chg_percent):
    predictions = []
    current_date = datetime.datetime.now()

    last_input = np.array([[price, open_price, high_price, low_price, volume, chg_percent]])

    for i in range(1, weeks_ahead + 1):
        scaled_input = scaler.transform(last_input)
        pred_raw = model.predict(scaled_input)
        predicted_price = float(pred_raw[0])

        week_date = current_date + datetime.timedelta(weeks=i)
        predictions.append({
            'date': week_date.strftime('%Y-%m-%d'),
            'predicted_price': round(predicted_price, 2)
        })

        # Adjust values for next week
        price_change = predicted_price - price
        open_price = predicted_price
        high_price = predicted_price + abs(price_change) * 0.5
        low_price = predicted_price - abs(price_change) * 0.5
        volume = volume * (1 + np.random.uniform(-0.02, 0.02))
        chg_percent = (predicted_price - price) / price * 100
        last_input = np.array([[predicted_price, open_price, high_price, low_price, volume, chg_percent]])
        price = predicted_price

    return predictions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    price = float(request.form['price'])
    open_price = float(request.form['open'])
    high_price = float(request.form['high'])
    low_price = float(request.form['low'])
    volume = float(request.form['volume'])
    chg_percent = float(request.form['chg_percent'])

    results = predict_future_prices(weeks_ahead=4, price=price, open_price=open_price,
                                    high_price=high_price, low_price=low_price,
                                    volume=volume, chg_percent=chg_percent)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
