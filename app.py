import streamlit as st
import requests
from datetime import datetime

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
    r = requests.post(RPC_URL, json=payload, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["result"]

def get_current_slot():
    return rpc_call("getSlot")

def get_block(slot):
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

# ---------------- RAYDIUM DETECTION ----------------
RAYDIUM_PROGRAM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"

def detect_raydium_activity(block):
    events = []
    if not block or "transactions" not in block:
        return events

    for tx in block["transactions"]:
        message = tx["transaction"]["message"]
        accounts = message.get("accountKeys", [])
        if any(
            acc.get("pubkey") == RAYDIUM_PROGRAM
            for acc in accounts
            if isinstance(acc, dict)
        ):
            events.append({
                "signature": tx.get("transaction", {}).get("signatures", [""])[0]
            })
    return events

# ---------------- UI ----------------
st.set_page_config(page_title="CTO Terminal 💻", layout="wide")
st.title("CTO Terminal 💻")
st.caption("We don’t chase pumps. We front-run them.")



if "last_slot" not in st.session_state:
    st.session_state.last_slot = None

try:
    current_slot = get_current_slot()
    events = []

    if current_slot != st.session_state.last_slot:
        block = get_block(current_slot)
        events = detect_raydium_activity(block)
        st.session_state.last_slot = current_slot

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

except Exception as e:
    st.error(f"RPC error: {e}")
    st.stop()

# ---------------- METRICS ----------------
c1, c2, c3 = st.columns(3)
c1.metric("Status", "LIVE 🟢")
c2.metric("Current Solana Slot", current_slot)
c3.metric("Raydium TXs (Slot)", len(events))

st.caption(f"Last update: {now}")

# ---------------- DETAILS ----------------
st.subheader("Raydium Activity (Confirmed)")

if events:
    st.success(f"⚡ {len(events)} Raydium interaction(s)")
    for e in events[:5]:
        st.markdown(f"- `{e['signature']}`")
else:
    st.info("No Raydium activity detected this slot")

st.divider()
st.caption("CTO Terminal V1 — real on-chain signals only")
import time
time.sleep(10)
st.rerun()