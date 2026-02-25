  import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

# ---------------- Database Setup ----------------
conn = sqlite3.connect("upi_streamlit.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS banks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    bank_name TEXT,
    account_number TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    bank_name TEXT,
    amount REAL,
    note TEXT,
    timestamp TEXT
)
""")
conn.commit()

# ---------------- Helpers ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, role="customer"):
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, hash_password(password), role))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

def get_user_banks(user_id):
    c.execute("SELECT * FROM banks WHERE user_id=?", (user_id,))
    return c.fetchall()

def add_bank(user_id, bank_name, account_number):
    c.execute("INSERT INTO banks (user_id, bank_name, account_number) VALUES (?, ?, ?)",
              (user_id, bank_name, account_number))
    conn.commit()

def add_transaction(user_id, bank_name, amount, note):
    c.execute("INSERT INTO transactions (user_id, bank_name, amount, note, timestamp) VALUES (?, ?, ?, ?, ?)",
              (user_id, bank_name, amount, note, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def get_transactions():
    c.execute("""SELECT t.id, u.username, t.bank_name, t.amount, t.note, t.timestamp
                 FROM transactions t
                 JOIN users u ON t.user_id = u.id""")
    return c.fetchall()

def get_all_users():
    c.execute("SELECT id, username, role FROM users")
    return c.fetchall()

# ---------------- App UI ----------------
st.title("💳 UPI Demo - Streamlit")

menu = ["Customer Login", "Customer Signup", "Admin Login"]
choice = st.sidebar.selectbox("Menu", menu)

# Customer Signup
if choice == "Customer Signup":
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        if add_user(username, password, "customer"):
            st.success("Account created successfully! Please login.")
        else:
            st.error("Username already exists!")

# Customer Login
elif choice == "Customer Login":
    st.subheader("Customer Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user and user[3] == "customer":
            st.success(f"Welcome {username}!")
            user_id = user[0]

            # Bank Section
            st.subheader("🏦 Your Banks")
            banks = get_user_banks(user_id)
            for b in banks:
                st.write(f"• {b[2]} - {b[3]}")

            bank_name = st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis", "PNB", "Canara", "Union Bank"])
            account_number = st.text_input("Account Number")
            if st.button("Add Bank"):
                add_bank(user_id, bank_name, account_number)
                st.success("Bank added successfully!")

            # Payment Section
            st.subheader("💸 Make a Payment")
            if banks:
                bank_choice = st.selectbox("Choose Bank", [b[2] for b in banks])
                amount = st.number_input("Amount", min_value=1.0)
                note = st.text_input("Note")
                if st.button("Pay"):
                    add_transaction(user_id, bank_choice, amount, note)
                    st.success("Payment Successful ✅")
            else:
                st.warning("Add a bank first!")

        else:
            st.error("Invalid credentials or not a customer!")

# Admin Login
elif choice == "Admin Login":
    st.subheader("Admin Login")
    username = st.text_input("Admin Username")
    password = st.text_input("Password", type="password")

    if st.button("Login as Admin"):
        user = login_user(username, password)
        if user and user[3] == "admin":
            st.success(f"Welcome Admin {username}")

            st.subheader("👥 Registered Users")
            users = get_all_users()
            st.table(users)

            st.subheader("💰 Transactions")
            txns = get_transactions()
            st.table(txns)

        else:
            st.error("Invalid admin credentials!")
