import streamlit as st
import requests
import os
import time

# Load RPC URL from environment variable (set in Railway/Fly secrets)
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
        return f"RPC Error: {str(e)}
