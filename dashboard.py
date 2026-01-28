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

# ── MUST BE THE VERY FIRST Streamlit command ──
st.set_page_config(
    page_title="CTO Terminal 💻",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS – fully closed, no placeholders
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