import streamlit as st
import requests
import time
from datetime import datetime

from raydium import detect_raydium_activity

RPC_URL = "https://go.getblock.us/d794c3db8dea44308057d167c1003c9a”

HEADERS = {"Content-Type": "application/json"}

def get_current_slot():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot",
        "params": []
    }
    res = requests.post(RPC_URL, json=payload, headers=HEADERS)
    return res.json()["result"]

def get_block(slot):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlock",
        "params": [
            slot,
            {
                "encoding": "jsonParsed",
                "transactionDetails": "full",
                "rewards": False
            }
        ]
    }
    res = requests.post(RPC_URL, json=payload, headers=HEADERS)
    return res.json()

# ---------------- UI ----------------

st.set_page_config(page_title="CTO Terminal", layout="wide")
st.title("CTO Terminal Live Dashboard 💻")
st.caption("We don’t chase pumps. We front-run them.")

if "last_slot" not in st.session_state:
    st.session_state.last_slot = None

current_slot = get_current_slot()
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

st.metric("Status", "LIVE 🟢")
st.metric("Current Solana Slot", current_slot)
st.caption(f"Last update: {now}")

if current_slot != st.session_state.last_slot:
    block = get_block(current_slot)
    events = detect_raydium_activity(block)

    if events:
        st.success(f"⚡ Raydium activity detected: {len(events)} txs")
        for e in events[:3]:
            st.write("Tx:", e["signature"])
            st.write("Mints:", ", ".join(e["mints"]) if e["mints"] else "Unknown")

    st.session_state.last_slot = current_slot

time.sleep(10)
st.rerun()
