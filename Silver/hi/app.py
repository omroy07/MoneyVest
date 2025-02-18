from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

def get_market_trend():
    """Determine if the silver market is up or down today."""
    try:
        silver = yf.Ticker("SI=F")
        history = silver.history(period="2d")  # Fetch last two days
        if len(history) < 2:
            return {"error": "Not enough data to determine market movement."}
        yesterday_close = history["Close"].iloc[-2]
        today_close = history["Close"].iloc[-1]
        movement = "Up" if today_close > yesterday_close else "Down"
        return {"yesterday_close": yesterday_close, "today_close": today_close, "movement": movement}
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/market_trend', methods=['GET'])
def market_trend():
    trend = get_market_trend()
    return jsonify(trend)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
