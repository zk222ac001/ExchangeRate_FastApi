import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Currency Finance Dashboard", layout="wide")

st.title("💰 Currency Finance Dashboard (Google Finance Style)")

# --------------------------
# Conversion Section
# --------------------------
col1, col2, col3 = st.columns(3)

from_currency = col1.text_input("From Currency", "USD")
to_currency = col2.text_input("To Currency", "EUR")
amount = col3.number_input("Amount", value=1.0)

if st.button("Convert"):
    res = requests.get(f"{API}/convert", params={
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount
    }).json()

    st.success(f"{amount} {from_currency} = {res['converted']} {to_currency}")
    st.info(f"Rate: {res['rate']}")

# --------------------------
# History Section
# --------------------------
st.subheader("📊 Exchange Rate History (Last 50)")

history = requests.get(f"{API}/history").json()

df = pd.DataFrame(history)

if not df.empty:
    st.dataframe(df)

    st.line_chart(df["rate"])
else:
    st.warning("No history yet")