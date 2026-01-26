import os
import requests
import time
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()

# --- CONFIGURATION FROM ENV ---
RPC_URL = os.getenv("RPC_URL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- RISK SETTINGS ---
SL_PERCENT = 0.85  # -15%
TP_PERCENT = 1.50  # +50%

watchlist = {} # Tracks {mint: entry_price}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

def fetch_current_price(mint):
    """Fetches real-time price from Dexscreener API"""
    url = f"https://api.dexscreener.com/latest/dex/tokens/{mint}"
    try:
        res = requests.get(url, timeout=10).json()
        if "pairs" in res and res["pairs"]:
            return float(res["pairs"][0]["priceUsd"])
    except:
        return None
    return None

def monitor_logic():
    """Checks your watched tokens for SL/TP hits"""
    for mint, entry_price in list(watchlist.items()):
        current = fetch_current_price(mint)
        if not current: continue
        
        perf = current / entry_price
        if perf <= SL_PERCENT:
            send_telegram(f"🛑 <b>STOP LOSS HIT</b>\nToken: <code>{mint}</code>\nExit: -15%")
            del watchlist[mint]
        elif perf >= TP_PERCENT:
            send_telegram(f"💰 <b>TAKE PROFIT HIT</b>\nToken: <code>{mint}</code>\nExit: +50%")
            del watchlist[mint]

# Main scouting logic from your original repo...
print(f"--- CTO TERMINAL v1.5 ACTIVE (Lagos Time: {time.strftime('%H:%M:%S')}) ---")
# Add your main loop here...
