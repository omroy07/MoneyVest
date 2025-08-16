from flask import Flask, render_template, request, jsonify
import math
import datetime

app = Flask(__name__)

# helper: convert compounding name to n
COMPOUND_MAP = {
    'yearly': 1,
    'quarterly': 4,
    'monthly': 12,
    'daily': 365
}

def compute_fd_schedule(principal, annual_rate, years, compounding, tax_rate=0.0, inflation=0.0):
    """
    Returns dict:
     - final_amount
     - gross_interest
     - tax_on_interest
     - net_amount_after_tax
     - real_amount (after inflation)
     - schedule: list of {'year': k, 'date': 'YYYY-MM-DD', 'balance': value}
    """
    n = COMPOUND_MAP.get(compounding, 12)
    r = annual_rate / 100.0
    t = years

    # Final amount
    A = principal * (1 + r / n) ** (n * t)
    gross_interest = A - principal
    tax_on_interest = (tax_rate / 100.0) * gross_interest
    net_amount_after_tax = A - tax_on_interest
    real_amount = A / ((1 + inflation / 100.0) ** t)

    # Year-by-year schedule (balances at end of each full year)
    schedule = []
    start_date = datetime.date.today()
    for year in range(1, int(math.ceil(t)) + 1):
        # compute amount at end of this year (year may exceed t if t not int; we clamp)
        yr = min(year, t)
        # use compound formula for yr years
        A_yr = principal * (1 + r / n) ** (n * yr)
        balance = round(A_yr, 2)
        date = (start_date + datetime.timedelta(weeks=52 * year)).isoformat()  # approximate week-based year
        schedule.append({'year': year, 'date': date, 'balance': balance})

    return {
        'final_amount': round(A, 2),
        'gross_interest': round(gross_interest, 2),
        'tax_on_interest': round(tax_on_interest, 2),
        'net_amount_after_tax': round(net_amount_after_tax, 2),
        'real_amount': round(real_amount, 2),
        'schedule': schedule
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        principal = float(request.form.get('principal', 0))
        annual_rate = float(request.form.get('annual_rate', 0))
        years = float(request.form.get('years', 1))
        compounding = request.form.get('compounding', 'monthly')
        tax_rate = float(request.form.get('tax_rate', 0))  # percent on interest
        inflation = float(request.form.get('inflation', 0))  # percent

        result = compute_fd_schedule(principal, annual_rate, years, compounding, tax_rate, inflation)
        # Return structured JSON
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True , port=5503)
