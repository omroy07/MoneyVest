from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def calculate_sip(amount, rate=12, years=10):
    try:
        amount = float(amount)
        if amount <= 0:
            return {"error": "Investment amount must be greater than zero."}
        
        monthly_rate = rate / 100 / 12
        months = years * 12
        total = 0
        data = []
        
        for i in range(1, months + 1):
            total = total * (1 + monthly_rate) + amount
            if i % 12 == 0:
                data.append({"year": i // 12, "value": round(total, 2)})
        
        return {"data": data}
    except ValueError:
        return {"error": "Invalid input. Please enter a valid number."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    amount = request.form.get('amount', '')
    result = calculate_sip(amount)
    
    if "error" in result:
        return jsonify(result)
    
    return jsonify({
        "label": "SIP Growth Over Time",
        "x_label": "Years",
        "y_label": "Investment Value (in currency)",
        "rate_info": "The calculation assumes a fixed annual return rate of 12% over 10 years.",
        "data": result["data"]
    })

if __name__ == '__main__':
    app.run(debug=True)

