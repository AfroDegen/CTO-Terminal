import streamlit as st
import requests
import os
import time

# Your GetBlock RPC (replace YOUR_API_KEY with your actual key for testing)
API_KEY = os.getenv("GETBLOCK_API_KEY", "YOUR_API_KEY_HERE_FOR_LOCAL_TEST")
RPC_URL = f"https://sol.getblock.io/mainnet/?api_key={API_KEY}"

def get_current_slot():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot",
        "params": []
    }
    try:
        response = requests.post(RPC_URL, json=payload).json()
        return response["result"]
    except:
        return "Error"

st.set_page_config(page_title="CTO Terminal", layout="wide")

st.title("CTO Terminal Dashboard 💻")
st.markdown("Real-time Solana monitoring | Building for @pumpdotfun hackathon")

st.subheader("Live Solana Status")

# Live updating slot
placeholder = st.empty()

while True:
    slot = get_current_slot()
    with placeholder.container():
        st.metric("Current Solana Slot", slot, delta=None)
    time.sleep(5)  # refreshes every 5 seconds