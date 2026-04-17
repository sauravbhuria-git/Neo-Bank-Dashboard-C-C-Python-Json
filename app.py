import streamlit as st
import json, os

DATA_FILE = "bank_data.json"

# ---------- FILE ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- INIT ----------
if not os.path.exists(DATA_FILE):
    save_data({})

# ---------- FUNCTIONS ----------
def create_account(acc_id, amount):
    data = load_data()
    if acc_id in data:
        return False
    data[acc_id] = {
        "balance": amount,
        "history": [f"Account {acc_id} created with ₹{amount}"],
        "loan": 0
    }
    save_data(data)
    return True

def deposit(acc_id, amt):
    data = load_data()
    if acc_id in data:
        data[acc_id]["balance"] += amt
        data[acc_id]["history"].append(f"Deposited ₹{amt}")
        save_data(data)

def withdraw(acc_id, amt):
    data = load_data()
    if acc_id in data and data[acc_id]["balance"] >= amt:
        data[acc_id]["balance"] -= amt
        data[acc_id]["history"].append(f"Withdrawn ₹{amt}")
        save_data(data)
        return True
    return False

def apply_loan(acc_id, amt):
    data = load_data()
    if acc_id in data:
        data[acc_id]["loan"] += amt
        data[acc_id]["history"].append(f"Loan Approved ₹{amt}")
        save_data(data)

# ---------- UI ----------
st.set_page_config(layout="wide")

st.markdown("""
<style>

/* BACKGROUND */
body {
    background: linear-gradient(120deg, #f6d365, #fda085);
}

/* HEADER */
.header {
    background: linear-gradient(90deg, #ff6a00, #ee0979, #00c6ff, #00ff87);
    padding: 18px;
    color: white;
    font-size: 28px;
    text-align: center;
    font-weight: bold;
    border-radius: 12px;
    letter-spacing: 1px;
}

/* PANEL */
.panel {
    background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
    color: #00ffcc;
    padding: 15px;
    border-radius: 12px;
    height: 420px;
    overflow-y: auto;
    font-family: monospace;
    border: 1px solid #00c6ff;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(45deg, #ff9a9e, #fad0c4, #fbc2eb, #a6c1ee);
    color: black;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

/* BUTTON HOVER */
.stButton>button:hover {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    transform: scale(1.05);
}

/* INPUT */
.stTextInput>div>div>input {
    background: #f0f8ff;
    border-radius: 8px;
    border: 2px solid #00c6ff;
}

.stNumberInput>div>div>input {
    background: #fff7e6;
    border-radius: 8px;
    border: 2px solid #ff6a00;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">🏦 Neo Bank Dashboard</div>', unsafe_allow_html=True)

# ---------- SESSION ----------
if "output" not in st.session_state:
    st.session_state.output = []

# ---------- INPUT ----------
col1, col2 = st.columns(2)
with col1:
    acc_id = st.text_input("Account ID")
with col2:
    amount = st.number_input("Amount", min_value=0)

# ---------- BUTTONS ----------
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

# CREATE
with col1:
    if st.button("➕ Create"):
        if create_account(acc_id, amount):
            st.session_state.output.append(f"✔ Account {acc_id} created with ₹{amount}")
        else:
            st.session_state.output.append("❌ Duplicate Account")

# DEPOSIT
with col2:
    if st.button("💰 Deposit"):
        deposit(acc_id, amount)
        st.session_state.output.append(f"✔ Deposited ₹{amount}")

# WITHDRAW
with col3:
    if st.button("💸 Withdraw"):
        if withdraw(acc_id, amount):
            st.session_state.output.append(f"✔ Withdrawn ₹{amount}")
        else:
            st.session_state.output.append("❌ Insufficient Balance")

# BALANCE
with col4:
    if st.button("📊 Balance"):
        data = load_data()
        if acc_id in data:
            bal = data[acc_id]["balance"]
            st.session_state.output.append(f"💰 Balance: ₹{bal}")
        else:
            st.session_state.output.append("❌ Account not found")

# TRANSACTIONS
with col5:
    if st.button("🧾 Transactions"):
        data = load_data()
        if acc_id in data:
            st.session_state.output.append("Recent Transactions:")
            for h in data[acc_id]["history"]:
                st.session_state.output.append("• " + h)
        else:
            st.session_state.output.append("❌ Account not found")

# BRANCH
with col6:
    if st.button("📍 Branch"):
        branches = [
            "Main Branch - Chandigarh",
            "Civil Lines - Ludhiana",
            "Model Town - Jalandhar",
            "City Center - Amritsar"
        ]
        st.session_state.output.append("Nearest Bank Branches:")
        for b in branches:
            st.session_state.output.append("• " + b)

# LOAN
with col7:
    if st.button("🏦 Loan"):
        data = load_data()
        if acc_id in data:
            apply_loan(acc_id, amount)
            st.session_state.output.append(f"✔ Loan Approved ₹{amount}")
        else:
            st.session_state.output.append("❌ Account not found")

# EMI
with col8:
    if st.button("📉 EMI"):
        rate = 10
        months = 12
        emi = (amount + (amount * rate / 100)) / months
        st.session_state.output.append(f"EMI: ₹{round(emi,2)} per month")

# ---------- OUTPUT ----------
st.markdown("### 💻 Console Output")

console_text = "<br>".join(st.session_state.output) if st.session_state.output else "System Ready..."

st.markdown(f'<div class="panel">{console_text}</div>', unsafe_allow_html=True)