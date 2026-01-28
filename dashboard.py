import streamlit as st
import requests
import os
import time

# Load RPC URL from environment variable
RPC_URL = os.getenv("SOLANA_RPC_URL")
if not RPC_URL:
    st.error("SOLANA_RPC_URL environment variable is not set! Add it in Railway Settings > Variables.")
    st.stop()

# Function to get current Solana slot
def get_current_slot():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot",
        "params": []
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10).json()
        if "result" in response:
            return response["result"]
        else:
            return f"Error: {response.get('error', 'Unknown')}"
    except Exception as e:
        return f"RPC Error: {str(e)}"

# Must be the very first Streamlit command
st.set_page_config(
    page_title="CTO Terminal 💻",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS – fully closed triple quotes, no issues
st.markdown("""
<style>
    /* Hide default footer/menu */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Neon glow on titles */
    h1, h2, h3 {
        color: #00D4FF !important;
        text-shadow: 0 0 10px #00D4FF80;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Card-like metrics & containers */
    div[data-testid="metric-container"] {
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        background-color: #111827;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.15);
    }

    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #334155;
        border-radius: 12px;
        background-color: #0F1624;
    }

    /* Better spacing */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Tagline style */
    .tagline {
        font-size: 1.3rem;
        color: #CBD5E1;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Title & Branding
st.markdown("<h1 style='text-align: center;'>CTO Terminal 💻</h1>", unsafe_allow_html=True)
st.markdown("<div class='tagline'>We don’t chase pumps. We front run them.</div>", unsafe_allow_html=True)
st.markdown("Real-time Solana monitoring for Comeback Token Opportunities (CTOs) | Building live for @pumpdotfun Pump Fund Hackathon")
st.markdown("Follow progress: [@CTOTERMINAL](https://x.com/CTOTERMINAL)")

# Sidebar
with st.sidebar:
    st.header("CTO Terminal")
    st.markdown("V1 in development")
    st.info("Monitoring pump.fun tokens for:\n- Sudden volume spikes\n- Liquidity injections\n- Early CTO signals")
    st.markdown("Follow progress: [@CTOTERMINAL](https://x.com/CTOTERMINAL)")
    refresh_rate = st.slider("Refresh interval (seconds)", 1, 30, 5)

# Main content
st.subheader("Live Solana Network Stats")
placeholder = st.empty()

# Auto-refresh loop
while True:
    with placeholder.container():
        slot = get_current_slot()
        st.metric(
            label="Current Solana Slot",
            value=slot if isinstance(slot, int) else slot,
            delta=None,
            help="Latest confirmed slot number from RPC"
        )

        st.subheader("Live Token Volume & CTO Alerts")
        st.info("Volume spikes & liquidity detection coming soon... (V1 in progress)")

        st.markdown("**Sample Token Monitoring** (demo)")
        sample_data = {
            "Token": ["EXAMPLE1", "EXAMPLE2"],
            "5min Volume": [45000, 12000],
            "Liq Added": [True, False],
            "CTO Score": ["High", "Medium"]
        }
        st.dataframe(sample_data, use_container_width=True)

    time.sleep(refresh_rate)