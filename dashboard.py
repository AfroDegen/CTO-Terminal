import streamlit as st
import requests
import os
import time
import json
import threading
import websocket  # Make sure to run: pip install websocket-client

# --- INITIAL CONFIG ---
st.set_page_config(
    page_title="CTO Terminal 💻",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- WEBSOCKET & STATE MANAGEMENT ---
# Initialize data storage if not present
if "pump_tokens" not in st.session_state:
    st.session_state.pump_tokens = []
if "data_lock" not in st.session_state:
    st.session_state.data_lock = threading.Lock()

def on_message(ws, message):
    data = json.loads(message)
    with st.session_state.data_lock:
        # Append new token and keep only the last 10
        st.session_state.pump_tokens.append(data)
        st.session_state.pump_tokens = st.session_state.pump_tokens[-10:]

def on_error(ws, error):
    print(f"WS Error: {error}")

def on_open(ws):
    # Subscribe to new token creations
    payload = {"method": "subscribeNewToken"}
    ws.send(json.dumps(payload))

def run_ws():
    ws = websocket.WebSocketApp(
        "wss://pumpportal.fun/api/data",
        on_message=on_message,
        on_error=on_error,
        on_open=on_open
    )
    ws.run_forever()

# Start WebSocket thread if it's not already running
if "ws_thread" not in st.session_state:
    st.session_state.ws_thread = threading.Thread(target=run_ws, daemon=True)
    st.session_state.ws_thread.start()

# --- ENVIRONMENT & RPC SETUP ---
RPC_URL = os.getenv("SOLANA_RPC_URL")

def get_current_slot():
    if not RPC_URL:
        return "RPC URL MISSING"
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getSlot", "params": []}
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10).json()
        return response.get("result", "Error")
    except Exception:
        return "RPC Error"

# --- CUSTOM CSS ---
st.markdown("""
<style>
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    h1, h2, h3 {
        color: #00D4FF !important;
        text-shadow: 0 0 10px #00D4FF80;
    }
    div[data-testid="metric-container"] {
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        background-color: #111827;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.15);
    }
    .hero-banner {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #00D4FF;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
    }
    .alert-box {
        background-color: #1e1b4b;
        border-left: 5px solid #00D4FF;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- UI COMPONENTS ---

st.markdown(
    """
    <div class="hero-banner">
        <h2 style='margin:0; color:#00D4FF;'>CTO Terminal – Front-Run Solana Comebacks</h2>
        <p style='color:#CBD5E1; font-size:1.1rem;'>Real-time detection of liquidity injections, volume spikes & wallet clusters</p>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("CTO Terminal")
    st.info("V1 Development: Live Pump.fun feed active.")
    refresh_rate = st.slider("UI Refresh interval (sec)", 1, 10, 3)
    st.markdown("---")
    st.markdown("Follow: [@CTOTERMINAL](https://x.com/CTOTERMINAL)")

# --- MAIN LOOP ---
placeholder = st.empty()

while True:
    with placeholder.container():
        slot = get_current_slot()
        
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric(label="Current Solana Slot", value=slot)
        with kpi2:
            st.metric(label="WS Status", value="Connected", delta="Live Feed")
        with kpi3:
            st.metric(label="Tokens Captured", value=len(st.session_state.pump_tokens))

        st.subheader("🔥 Live Pump.fun Activity")
        
        if st.session_state.pump_tokens:
            # Display latest tokens in a clean JSON format or table
            for token in reversed(st.session_state.pump_tokens[-3:]):
                with st.expander(f"New Token: {token.get('name', 'Unknown')}"):
                    st.json(token)
        else:
            st.info("Waiting for new tokens from PumpPortal...")

        st.markdown("---")
        st.caption("CTO Terminal 💻 | Solo build from Ibadan 🇳🇬")

    time.sleep(refresh_rate)
