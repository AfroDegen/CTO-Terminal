import streamlit as st
import requests
import os
import time
import json
import threading
import websocket

# --- INITIAL CONFIG ---
st.set_page_config(
    page_title="CTO Terminal 💻",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- WEBSOCKET & STATE MANAGEMENT ---
if "pump_tokens" not in st.session_state:
    st.session_state.pump_tokens = []
if "data_lock" not in st.session_state:
    st.session_state.data_lock = threading.Lock()

def on_message(ws, message):
    try:
        data = json.loads(message)
        # We only care about new token creations for this feed
        if data.get("txType") == "create" or "mint" in data:
            with st.session_state.data_lock:
                st.session_state.pump_tokens.append(data)
                # Keep only last 20 tokens to save memory
                st.session_state.pump_tokens = st.session_state.pump_tokens[-20:]
    except Exception as e:
        pass

def run_ws():
    ws = websocket.WebSocketApp(
        "wss://pumpportal.fun/api/data",
        on_message=on_message,
        on_open=lambda ws: ws.send(json.dumps({"method": "subscribeNewToken"}))
    )
    ws.run_forever()

if "ws_thread" not in st.session_state:
    st.session_state.ws_thread = threading.Thread(target=run_ws, daemon=True)
    st.session_state.ws_thread.start()

# --- RPC SETUP ---
RPC_URL = os.getenv("SOLANA_RPC_URL")
def get_current_slot():
    if not RPC_URL: return "---"
    try:
        r = requests.post(RPC_URL, json={"jsonrpc":"2.0","id":1,"method":"getSlot"}, timeout=5)
        return r.json().get("result", "Error")
    except: return "Error"

# --- STYLING & HELPERS ---
st.markdown("""
<style>
    footer {visibility: hidden;}
    h1, h2, h3 { color: #00D4FF !important; text-shadow: 0 0 10px #00D4FF80; }
    
    .hero-banner {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #00D4FF;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }

    .token-card {
        background-color: #111827;
        border: 1px solid #334155;
        border-left: 5px solid #00D4FF;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }

    .view-btn {
        background-color: #00D4FF;
        border: none;
        color: black;
        padding: 8px;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        text-align: center;
        display: block;
        text-decoration: none;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

def render_token_card(token):
    name = token.get("name", "Unknown")
    symbol = token.get("symbol", "???")
    mint = token.get("mint", "N/A")
    st.markdown(f"""
    <div class="token-card">
        <div style="display:flex; justify-content:space-between;">
            <span style="color:white; font-weight:bold;">{name}</span>
            <span style="color:#00D4FF; font-size:0.8rem;">{symbol}</span>
        </div>
        <div style="color:#94a3b8; font-size:0.8rem; margin-top:5px;">
            Mint: <code>{mint[:4]}...{mint[-4:]}</code>
        </div>
        <a class="view-btn" href="https://pump.fun/{mint}" target="_blank">TRADE ON PUMP.FUN</a>
    </div>
    """, unsafe_allow_html=True)

# --- UI LAYOUT ---
st.markdown('<div class="hero-banner"><h2>CTO Terminal 💻</h2><p>Front-running Solana Comebacks Live</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings")
    refresh_rate = st.slider("UI Refresh (s)", 2, 10, 3)
    st.info("WebSocket: Connected 🟢")

placeholder = st.empty()

while True:
    with placeholder.container():
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Solana Slot", get_current_slot())
        m2.metric("New Tokens", len(st.session_state.pump_tokens))
        m3.metric("Terminal Status", "Scanning", delta="Live")

        st.subheader("🔥 Live Pump.fun Feed")
        if st.session_state.pump_tokens:
            cols = st.columns(2)
            # Show last 6 tokens
            for i, token in enumerate(reversed(st.session_state.pump_tokens[-6:])):
                with cols[i % 2]:
                    render_token_card(token)
        else:
            st.warning("Waiting for new token launches...")

    time.sleep(refresh_rate)
