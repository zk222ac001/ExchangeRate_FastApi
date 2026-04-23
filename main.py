from fastapi import FastAPI
import requests
import sqlite3
from datetime import datetime

app = FastAPI(title="Currency Finance API")

BASE_URL = "https://api.exchangerate-api.com/v4/latest/"

# --------------------------
# DB Setup
# --------------------------
conn = sqlite3.connect("currency.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_currency TEXT,
    to_currency TEXT,
    rate REAL,
    timestamp TEXT
)
""")
conn.commit()

# --------------------------
# Helper Function
# --------------------------
def save_history(from_c, to_c, rate):
    cursor.execute(
        "INSERT INTO history (from_currency, to_currency, rate, timestamp) VALUES (?, ?, ?, ?)",
        (from_c, to_c, rate, datetime.now().isoformat())
    )
    conn.commit()

# --------------------------
# Live Conversion
# --------------------------
@app.get("/convert")
def convert(from_currency: str, to_currency: str, amount: float = 1):
    data = requests.get(f"{BASE_URL}{from_currency.upper()}").json()
    rate = data["rates"][to_currency.upper()]

    result = amount * rate

    save_history(from_currency, to_currency, rate)

    return {
        "from": from_currency,
        "to": to_currency,
        "rate": rate,
        "amount": amount,
        "converted": result
    }

# --------------------------
# History API
# --------------------------
@app.get("/history")
def history():
    cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "from": r[1],
            "to": r[2],
            "rate": r[3],
            "time": r[4]
        }
        for r in rows
    ]