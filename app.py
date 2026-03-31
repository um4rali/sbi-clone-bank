from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import datetime
import json
import os
import hashlib
import secrets
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sbi-clone-bank-secret-key-2024'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)

# ====================== BANK CONFIGURATION ======================
BANK_NAME = "STATE BANK OF INDIA"
BANK_SHORT_NAME = "SBI"
BANK_SLOGAN = "The Nation banks on us"
BANK_ADDRESS = "State Bank Bhawan, Madame Cama Road, Mumbai - 400021"
BANK_PHONE = "1800 11 2211"
BANK_EMAIL = "contactcentre@sbi.co.in"
BANK_WEBSITE = "www.sbi.co.in"
BANK_CIN = "L65110MH1955GOI007112"
BANK_IFSC = "SBIN0000001"
BANK_MICR = "400002001"

# ====================== DATA STORAGE ======================
DATA_FILE = 'data/users.json'
ACCOUNTS_FILE = 'data/accounts.json'
TRANSACTIONS_FILE = 'data/transactions.json'

# Initialize data files
def init_data_files():
    # Create data directory if not exists
    os.makedirs('data', exist_ok=True)
    
    # Users file
    if not os.path.exists(DATA_FILE):
        default_users = {
            "rajesh.kumar": {
                "password": generate_password_hash("Rajesh@123"),
                "full_name": "Rajesh Kumar",
                "email": "rajesh.kumar@email.com",
                "phone": "9876543210",
                "pan": "ABCDE1234F",
                "aadhar": "123412341234",
                "dob": "1985-06-15",
                "address": "45, Green Park Extension, New Delhi - 110016",
                "occupation": "Software Engineer",
                "gender": "Male",
                "marital_status": "Married",
                "nominee_name": "Priya Kumar",
                "nominee_relation": "Spouse"
            },
            "priya.sharma": {
                "password": generate_password_hash("Priya@456"),
                "full_name": "Priya Sharma",
                "email": "priya.sharma@email.com",
                "phone": "9876543211",
                "pan": "FGHIJ5678K",
                "aadhar": "567856785678",
                "dob": "1990-09-22",
                "address": "101, Marine Drive, Mumbai - 400002",
                "occupation": "Doctor",
                "gender": "Female",
                "marital_status": "Single",
                "nominee_name": "Amit Sharma",
                "nominee_relation": "Father"
            },
            "amit.patel": {
                "password": generate_password_hash("Amit@789"),
                "full_name": "Amit Patel",
                "email": "amit.patel@email.com",
                "phone": "9876543212",
                "pan": "KLMNO9012P",
                "aadhar": "901290129012",
                "dob": "1982-03-10",
                "address": "22, Cunningham Road, Bangalore - 560052",
                "occupation": "Business Owner",
                "gender": "Male",
                "marital_status": "Married",
                "nominee_name": "Neha Patel",
                "nominee_relation": "Spouse"
            }
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(default_users, f, indent=4)
    
    # Accounts file
    if not os.path.exists(ACCOUNTS_FILE):
        default_accounts = {
            "12345678901": {
                "username": "rajesh.kumar",
                "account_type": "Savings Account",
                "account_number": "12345678901",
                "ifsc_code": "SBIN0001234",
                "branch": "Green Park, New Delhi",
                "balance": 154280.50,
                "opening_date": "2015-04-10",
                "status": "active",
                "daily_limit": 50000,
                "transfer_limit": 25000,
                "nominee_registered": True,
                "interest_rate": "3.50%",
                "last_transaction": "2024-02-15"
            },
            "12345678902": {
                "username": "rajesh.kumar",
                "account_type": "Fixed Deposit",
                "account_number": "12345678902",
                "ifsc_code": "SBIN0001234",
                "branch": "Green Park, New Delhi",
                "balance": 500000.00,
                "opening_date": "2023-01-15",
                "maturity_date": "2024-01-15",
                "status": "active",
                "interest_rate": "7.20%",
                "fd_period": "12 months"
            },
            "23456789012": {
                "username": "priya.sharma",
                "account_type": "Salary Account",
                "account_number": "23456789012",
                "ifsc_code": "SBIN0000456",
                "branch": "Marine Drive, Mumbai",
                "balance": 87500.75,
                "opening_date": "2020-08-21",
                "status": "active",
                "daily_limit": 100000,
                "transfer_limit": 50000,
                "nominee_registered": False,
                "interest_rate": "3.00%",
                "last_transaction": "2024-02-14"
            },
            "34567890123": {
                "username": "amit.patel",
                "account_type": "Current Account",
                "account_number": "34567890123",
                "ifsc_code": "SBIN0000789",
                "branch": "Cunningham Road, Bangalore",
                "balance": 1250000.00,
                "opening_date": "2018-11-05",
                "status": "active",
                "daily_limit": 500000,
                "transfer_limit": 200000,
                "nominee_registered": True,
                "interest_rate": "2.50%",
                "last_transaction": "2024-02-15"
            }
        }
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump(default_accounts, f, indent=4)
    
    # Transactions file
    if not os.path.exists(TRANSACTIONS_FILE):
        default_transactions = {
            "12345678901": [
                {"date": "2024-02-15", "description": "Amazon Pay", "amount": 2499.00, "type": "debit", "mode": "UPI", "reference": "UPI" + secrets.token_hex(4).upper(), "balance": 154280.50},
                {"date": "2024-02-14", "description": "Salary Credit", "amount": 75000.00, "type": "credit", "mode": "NEFT", "reference": "NEFT" + secrets.token_hex(4).upper(), "balance": 156779.50},
                {"date": "2024-02-12", "description": "Electricity Bill", "amount": 2345.00, "type": "debit", "mode": "Bill Pay", "reference": "BILL" + secrets.token_hex(4).upper(), "balance": 81779.50},
                {"date": "2024-02-10", "description": "Zomato", "amount": 856.00, "type": "debit", "mode": "Debit Card", "reference": "POS" + secrets.token_hex(4).upper(), "balance": 84124.50},
                {"date": "2024-02-08", "description": "Transfer from FD", "amount": 50000.00, "type": "credit", "mode": "Transfer", "reference": "TFR" + secrets.token_hex(4).upper(), "balance": 84980.50},
            ],
            "23456789012": [
                {"date": "2024-02-14", "description": "ATM Withdrawal", "amount": 5000.00, "type": "debit", "mode": "ATM", "reference": "ATM" + secrets.token_hex(4).upper(), "balance": 87500.75},
                {"date": "2024-02-12", "description": "Salary Credit", "amount": 95000.00, "type": "credit", "mode": "NEFT", "reference": "NEFT" + secrets.token_hex(4).upper(), "balance": 92500.75},
                {"date": "2024-02-10", "description": "Phone Bill", "amount": 1499.00, "type": "debit", "mode": "AutoPay", "reference": "AUTO" + secrets.token_hex(4).upper(), "balance": -2500.25},
            ],
            "34567890123": [
                {"date": "2024-02-15", "description": "GST Payment", "amount": 18500.00, "type": "debit", "mode": "RTGS", "reference": "RTGS" + secrets.token_hex(4).upper(), "balance": 1250000.00},
                {"date": "2024-02-14", "description": "Client Payment", "amount": 350000.00, "type": "credit", "mode": "NEFT", "reference": "NEFT" + secrets.token_hex(4).upper(), "balance": 1268500.00},
                {"date": "2024-02-12", "description": "Rent Received", "amount": 45000.00, "type": "credit", "mode": "UPI", "reference": "UPI" + secrets.token_hex(4).upper(), "balance": 918500.00},
            ]
        }
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump(default_transactions, f, indent=4)

# Initialize all data files
init_data_files()

# ====================== HELPER FUNCTIONS ======================
def load_users():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_accounts():
    with open(ACCOUNTS_FILE, 'r') as f:
        return json.load(f)

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=4)

def load_transactions():
    with open(TRANSACTIONS_FILE, 'r') as f:
        return json.load(f)

def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, 'w') as f:
        json.dump(transactions, f, indent=4)

def generate_account_number():
    """Generate a unique 11-digit account number"""
    accounts = load_accounts()
    while True:
        acc_num = ''.join([str(secrets.randbelow(10)) for _ in range(11)])
        if acc_num not in accounts:
            return acc_num

def mask_account_number(acc_num):
    """Mask account number for display (show last 4 digits)"""
    if len(acc_num) >= 8:
        return "XXXXXX" + acc_num[-4:]
    return acc_num

def format_currency(amount):
    """Format amount in Indian currency style"""
    return "₹{:,.2f}".format(amount)

def validate_pan(pan):
    """Validate PAN card format"""
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return re.match(pattern, pan) is not None

def validate_aadhar(aadhar):
    """Validate Aadhar number"""
    pattern = r'^\d{12}$'
    return re.match(pattern, aadhar) is not None

def validate_mobile(mobile):
    """Validate mobile number"""
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, mobile) is not None

def validate_email(email):
    """Validate email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ====================== DECORATORS ======================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def utility_processor():
    """Make utility functions available in templates"""
    return dict(
        now=datetime.datetime.now,
        mask_account=mask_account_number,
        format_currency=format_currency
    )

# ====================== ROUTES ======================

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html',
                         bank_name=BANK_NAME,
                         short_name=BANK_SHORT_NAME,
                         slogan=BANK_SLOGAN)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = load_users()
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            session['logged_in'] = True
            session['login_time'] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            session['ip_address'] = request.remote_addr
            
            flash(f'Welcome back, {users[username]["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html', bank_name=BANK_NAME)

# GET endpoint for Hydra demonstration
@app.route('/api/auth', methods=['GET'])
def api_auth():
    """Authentication endpoint - GET method for Hydra demo"""
    users = load_users()
    username = request.args.get('username')
    password = request.args.get('password')
    
    if username in users and check_password_hash(users[username]['password'], password):
        return jsonify({
            'status': 'success',
            'message': 'Authentication successful',
            'user': username,
            'name': users[username]['full_name']
        })
    else:
        return jsonify({
            'status': 'failed',
            'message': 'Invalid credentials'
        }), 401

@app.route('/register', methods=['GET', 'POST'])
def register():
    """New user registration"""
    if request.method == 'POST':
        users = load_users()
        accounts = load_accounts()
        
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        pan = request.form.get('pan')
        aadhar = request.form.get('aadhar')
        dob = request.form.get('dob')
        address = request.form.get('address')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        if not validate_email(email):
            flash('Invalid email format.', 'danger')
            return redirect(url_for('register'))
        
        if not validate_mobile(phone):
            flash('Invalid mobile number. Must be 10 digits starting with 6-9.', 'danger')
            return redirect(url_for('register'))
        
        if not validate_pan(pan.upper()):
            flash('Invalid PAN card format. (e.g., ABCDE1234F)', 'danger')
            return redirect(url_for('register'))
        
        if not validate_aadhar(aadhar):
            flash('Invalid Aadhar number. Must be 12 digits.', 'danger')
            return redirect(url_for('register'))
        
        # Check if username already exists
        username = email.split('@')[0].lower()
        if username in users:
            flash('Username already exists. Please use different email.', 'danger')
            return redirect(url_for('register'))
        
        # Check if PAN already registered
        for user_data in users.values():
            if user_data.get('pan') == pan.upper():
                flash('PAN card already registered with another account.', 'danger')
                return redirect(url_for('register'))
        
        # Create new user
        new_user = {
            "password": generate_password_hash(password),
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "pan": pan.upper(),
            "aadhar": aadhar,
            "dob": dob,
            "address": address,
            "occupation": request.form.get('occupation', ''),
            "gender": request.form.get('gender', ''),
            "marital_status": request.form.get('marital_status', ''),
            "nominee_name": request.form.get('nominee_name', ''),
            "nominee_relation": request.form.get('nominee_relation', ''),
            "registration_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users[username] = new_user
        save_users(users)
        
        # Create savings account
        account_number = generate_account_number()
        new_account = {
            "username": username,
            "account_type": "Savings Account",
            "account_number": account_number,
            "ifsc_code": "SBIN000" + ''.join([str(secrets.randbelow(10)) for _ in range(4)]),
            "branch": "Main Branch",
            "balance": 5000.00,  # Initial deposit
            "opening_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "status": "active",
            "daily_limit": 50000,
            "transfer_limit": 25000,
            "nominee_registered": bool(request.form.get('nominee_name')),
            "interest_rate": "3.50%"
        }
        
        accounts[account_number] = new_account
        save_accounts(accounts)
        
        # Create welcome transaction
        transactions = load_transactions()
        transactions[account_number] = [
            {
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "description": "Welcome Bonus",
                "amount": 5000.00,
                "type": "credit",
                "mode": "Deposit",
                "reference": "WEL" + secrets.token_hex(4).upper(),
                "balance": 5000.00
            }
        ]
        save_transactions(transactions)
        
        print(f"\n{'='*60}")
        print(f"✅ NEW ACCOUNT OPENED - {bank_name}")
        print(f"{'='*60}")
        print(f"Customer: {full_name}")
        print(f"Username: {username}")
        print(f"Account: {account_number}")
        print(f"IFSC: {new_account['ifsc_code']}")
        print(f"Initial Balance: ₹5,000.00")
        print(f"{'='*60}\n")
        
        flash('Account created successfully! Please login with your username.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', bank_name=BANK_NAME)

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard after login"""
    username = session['username']
    users = load_users()
    accounts = load_accounts()
    transactions = load_transactions()
    
    user = users[username]
    
    # Get user's accounts
    user_accounts = []
    for acc_num, acc_data in accounts.items():
        if acc_data['username'] == username:
            user_accounts.append(acc_data)
    
    # Get primary account (first savings account)
    primary_account = None
    for acc in user_accounts:
        if acc['account_type'] == 'Savings Account':
            primary_account = acc
            break
    
    if not primary_account and user_accounts:
        primary_account = user_accounts[0]
    
    # Get recent transactions
    recent_transactions = []
    if primary_account:
        all_transactions = transactions.get(primary_account['account_number'], [])
        recent_transactions = all_transactions[-5:] if all_transactions else []
        recent_transactions = list(reversed(recent_transactions))
    
    # Calculate total balance
    total_balance = sum(acc['balance'] for acc in user_accounts)
    
    return render_template('dashboard.html',
                         bank_name=BANK_NAME,
                         short_name=BANK_SHORT_NAME,
                         user=user,
                         accounts=user_accounts,
                         primary_account=primary_account,
                         total_balance=total_balance,
                         transactions=recent_transactions,
                         transaction_count=len(recent_transactions))

@app.route('/accounts')
@login_required
def accounts():
    """View all accounts"""
    username = session['username']
    accounts = load_accounts()
    
    user_accounts = []
    for acc_num, acc_data in accounts.items():
        if acc_data['username'] == username:
            user_accounts.append(acc_data)
    
    return render_template('accounts.html',
                         bank_name=BANK_NAME,
                         accounts=user_accounts)

@app.route('/account/<account_number>')
@login_required
def account_details(account_number):
    """View specific account details"""
    username = session['username']
    accounts = load_accounts()
    transactions = load_transactions()
    
    if account_number not in accounts or accounts[account_number]['username'] != username:
        flash('Account not found.', 'danger')
        return redirect(url_for('accounts'))
    
    account = accounts[account_number]
    account_transactions = transactions.get(account_number, [])
    account_transactions = list(reversed(account_transactions))
    
    return render_template('account-details.html',
                         bank_name=BANK_NAME,
                         account=account,
                         transactions=account_transactions)

@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    """Money transfer page - INSECURE for mitmproxy demo"""
    username = session['username']
    accounts = load_accounts()
    transactions = load_transactions()
    
    # Get user's accounts
    user_accounts = []
    for acc_num, acc_data in accounts.items():
        if acc_data['username'] == username:
            user_accounts.append(acc_data)
    
    if request.method == 'POST':
        from_account = request.form.get('from_account')
        to_account = request.form.get('to_account')
        amount = request.form.get('amount')
        remarks = request.form.get('remarks', '')
        mode = request.form.get('mode', 'NEFT')
        
        # Validation
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                flash('Please enter a valid amount.', 'danger')
                return redirect(url_for('transfer'))
            
            # Check if from account belongs to user
            if from_account not in accounts or accounts[from_account]['username'] != username:
                flash('Invalid source account.', 'danger')
                return redirect(url_for('transfer'))
            
            # Check balance
            if accounts[from_account]['balance'] < amount_float:
                flash('Insufficient balance.', 'danger')
                return redirect(url_for('transfer'))
            
            # Check daily limit
            if amount_float > accounts[from_account]['daily_limit']:
                flash(f'Amount exceeds daily limit of {format_currency(accounts[from_account]["daily_limit"])}', 'danger')
                return redirect(url_for('transfer'))
            
        except ValueError:
            flash('Please enter a valid amount.', 'danger')
            return redirect(url_for('transfer'))
        
        # 🔴 INSECURE: Log the transaction in plain text for mitmproxy demo
        print(f"\n{'🔴'*60}")
        print(f"INSECURE TRANSACTION DETECTED - MITM DEMO")
        print(f"{'🔴'*60}")
        print(f"From Account: {from_account}")
        print(f"To Account: {to_account}")
        print(f"Amount: ₹{amount}")
        print(f"Remarks: {remarks}")
        print(f"Mode: {mode}")
        print(f"Timestamp: {datetime.datetime.now()}")
        print(f"{'🔴'*60}\n")
        
        # Process transfer
        accounts[from_account]['balance'] -= amount_float
        
        # Add transaction for sender
        if from_account not in transactions:
            transactions[from_account] = []
        
        transactions[from_account].append({
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "description": f"Transfer to {mask_account_number(to_account)} - {remarks}",
            "amount": -amount_float,
            "type": "debit",
            "mode": mode,
            "reference": "TXN" + secrets.token_hex(4).upper(),
            "balance": accounts[from_account]['balance']
        })
        
        # Update recipient account if exists in our system
        if to_account in accounts:
            accounts[to_account]['balance'] += amount_float
            
            if to_account not in transactions:
                transactions[to_account] = []
            
            transactions[to_account].append({
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "description": f"Transfer from {mask_account_number(from_account)} - {remarks}",
                "amount": amount_float,
                "type": "credit",
                "mode": mode,
                "reference": "TXN" + secrets.token_hex(4).upper(),
                "balance": accounts[to_account]['balance']
            })
        
        save_accounts(accounts)
        save_transactions(transactions)
        
        flash(f'Transfer of {format_currency(amount_float)} initiated successfully.', 'success')
        return redirect(url_for('transfer_success', 
                              to_account=to_account,
                              amount=amount,
                              remarks=remarks,
                              reference=transactions[from_account][-1]['reference']))
    
    return render_template('transfer.html',
                         bank_name=BANK_NAME,
                         accounts=user_accounts)

@app.route('/transfer/success')
@login_required
def transfer_success():
    """Transfer success page"""
    to_account = request.args.get('to_account')
    amount = request.args.get('amount')
    remarks = request.args.get('remarks', '')
    reference = request.args.get('reference')
    
    return render_template('transfer-success.html',
                         bank_name=BANK_NAME,
                         to_account=to_account,
                         amount=amount,
                         remarks=remarks,
                         reference=reference)

@app.route('/profile')
@login_required
def profile():
    """User profile"""
    username = session['username']
    users = load_users()
    accounts = load_accounts()
    
    user = users[username]
    
    # Get user's accounts
    user_accounts = []
    for acc_num, acc_data in accounts.items():
        if acc_data['username'] == username:
            user_accounts.append(acc_data)
    
    return render_template('profile.html',
                         bank_name=BANK_NAME,
                         user=user,
                         accounts=user_accounts)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update profile information"""
    username = session['username']
    users = load_users()
    
    # Update allowed fields
    users[username]['phone'] = request.form.get('phone')
    users[username]['address'] = request.form.get('address')
    users[username]['occupation'] = request.form.get('occupation')
    
    save_users(users)
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('profile'))

@app.route('/statements')
@login_required
def statements():
    """Account statements"""
    username = session['username']
    accounts = load_accounts()
    
    user_accounts = []
    for acc_num, acc_data in accounts.items():
        if acc_data['username'] == username:
            user_accounts.append(acc_data)
    
    return render_template('statements.html',
                         bank_name=BANK_NAME,
                         accounts=user_accounts)

@app.route('/api/statement/<account_number>')
@login_required
def get_statement(account_number):
    """Get account statement as JSON"""
    username = session['username']
    accounts = load_accounts()
    transactions = load_transactions()
    
    if account_number not in accounts or accounts[account_number]['username'] != username:
        return jsonify({'error': 'Account not found'}), 404
    
    account = accounts[account_number]
    account_transactions = transactions.get(account_number, [])
    
    return jsonify({
        'account': account,
        'transactions': account_transactions
    })

@app.route('/beneficiaries')
@login_required
def beneficiaries():
    """Manage beneficiaries"""
    return render_template('beneficiaries.html', bank_name=BANK_NAME)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# API endpoint for account validation
@app.route('/api/validate-account/<account_number>')
def validate_account(account_number):
    """Check if account exists (for transfer)"""
    accounts = load_accounts()
    
    if account_number in accounts:
        return jsonify({
            'valid': True,
            'name': accounts[account_number]['account_type'],
            'ifsc': accounts[account_number]['ifsc_code']
        })
    
    # Simulate external bank account (for demo)
    if len(account_number) == 11 and account_number.isdigit():
        return jsonify({
            'valid': True,
            'name': 'External Account',
            'ifsc': 'SBIN000XXXX'
        })
    
    return jsonify({'valid': False})

if __name__ == '__main__':
    print("\n" + "="*70)
    print(f"🏦 {BANK_NAME}")
    print("="*70)
    print(f"🌐 Server: http://localhost:5000")
    print(f"\n📝 Demo Login Credentials:")
    print(f"   Username: rajesh.kumar | Password: Rajesh@123")
    print(f"   Username: priya.sharma | Password: Priya@456")
    print(f"   Username: amit.patel   | Password: Amit@789")
    print(f"\n🔴 INSECURE ENDPOINTS (For Hydra & mitmproxy Demo):")
    print(f"   Hydra Target: http://localhost:5000/api/auth?username=rajesh.kumar&password=Rajesh@123")
    print(f"   mitmproxy: Transfer page sends data in plain text")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
