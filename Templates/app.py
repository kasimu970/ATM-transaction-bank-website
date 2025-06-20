app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'secret123'

# Sample user database (in-memory)
users = {
    "123456": {
        "pin": "1234",
        "balance": 1000.00,
        "transactions": []
    }
}

admin_pin = "admin123"  # Admin PIN for verification

# Home/Login Page
@app.route('/')
def home():
    return render_template('login.html')

# Handle Login
@app.route('/login', methods=['POST'])
def login():
    account = request.form['account']
    pin = request.form['pin']

    if account in users and users[account]['pin'] == pin:
        session['account'] = account
        return redirect(url_for('verify_admin'))
    else:
        flash("Invalid account number or PIN", "danger")
        return redirect(url_for('home'))

# Admin Verification Page
@app.route('/verify', methods=['GET', 'POST'])
def verify_admin():
    if request.method == 'POST':
        pin = request.form['admin_pin']
        if pin == admin_pin:
            return redirect(url_for('dashboard'))
        else:
            flash("Admin verification failed", "danger")
            return redirect(url_for('verify_admin'))
    return render_template('verify.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'account' not in session:
        return redirect(url_for('home'))
    acc = session['account']
    return render_template('dashboard.html', account=acc, balance=users[acc]['balance'])

# View Transactions
@app.route('/transactions')
def transaction_history():
    if 'account' not in session:
        return redirect(url_for('home'))
    acc = session['account']
    return render_template('transaction.html', transactions=users[acc]['transactions'])

# Deposit Route
@app.route('/deposit', methods=['POST'])
def deposit():
    if 'account' not in session:
        return redirect(url_for('home'))
    acc = session['account']
    try:
        amount = float(request.form['amount'])
        users[acc]['balance'] += amount
        users[acc]['transactions'].append(f"Deposited ${amount:.2f}")
    except ValueError:
        flash("Invalid amount", "danger")
    return redirect(url_for('dashboard'))

# Withdraw Route
@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'account' not in session:
        return redirect(url_for('home'))
    acc = session['account']
    try:
        amount = float(request.form['amount'])
        if users[acc]['balance'] >= amount:
            users[acc]['balance'] -= amount
            users[acc]['transactions'].append(f"Withdrew ${amount:.2f}")
        else:
            flash("Insufficient balance", "danger")
    except ValueError:
        flash("Invalid amount", "danger")
    return redirect(url_for('dashboard'))

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
python 