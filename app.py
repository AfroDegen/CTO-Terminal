import streamlit as st
import requests
from datetime import datetime

from raydium import detect_raydium_activity

# ---------------- CONFIG ----------------

RPC_URL = "https://go.getblock.us/d794c3db8dea44308057d167c1003c9a"
HEADERS = {"Content-Type": "application/json"}

REFRESH_MS = 10_000  # 10 seconds

# ---------------- RPC HELPERS ----------------

def rpc_call(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or []
    }
    res = requests.post(RPC_URL, json=payload, headers=HEADERS, timeout=10)
    res.raise_for_status()
    return res.json()["result"]

def get_current_slot():
    return rpc_call("getSlot")

def get_block(slot: int):
    return rpc_call(
        "getBlock",
        [
            slot,
            {
                "encoding": "jsonParsed",
                "transactionDetails": "full",
                "rewards": False
            }
        ]
    )

# ---------------- UI ----------------

st.set_page_config(
    page_title="CTO Terminal 💻",
    layout="wide"
)

st.title("CTO Terminal 💻")
st.caption("We don’t chase pumps. We front-run them.")

# Auto refresh (SAFE way)
st.autorefresh(interval=REFRESH_MS, key="ctorefresh")

# Session state
if "last_slot" not in st.session_state:
    st.session_state.last_slot = None

# ---------------- DATA ----------------

try:
    current_slot = get_current_slot()
    block = None
    events = []

    if current_slot != st.session_state.last_slot:
        block = get_block(current_slot)
        events = detect_raydium_activity(block)
        st.session_state.last_slot = current_slot

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

except Exception as e:
    st.error(f"RPC Error: {e}")
    st.stop()

# ---------------- METRICS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Status", "LIVE 🟢")

with col2:
    st.metric("Current Solana Slot", current_slot)

with col3:
    st.metric("Raydium TXs (This Slot)", len(events))

st.caption(f"Last update: {now}")

# ---------------- DETAILS ----------------

st.subheader("Raydium Activity (Live)")

if events:
    st.success(f"⚡ {len(events)} Raydium transactions detected")
    for e in events[:5]:
        st.markdown(f"- **Tx:** `{e.get('signature')}`")
        mints = e.get("mints") or []
        if mints:
            st.caption("Mints: " + ", ".join(mints))
else:
    st.info("No Raydium activity detected in this slot")

st.divider()

st.caption("CTO Terminal V1 — live on-chain signal detection")