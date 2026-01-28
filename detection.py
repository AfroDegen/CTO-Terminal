```python
import requests
import time
from datetime import datetime, timedelta

# Configuration
SOLANA_RPC = "https://api.mainnet-beta.solana.com"
VOLUME_THRESHOLD = 2.0  # 200% increase
CHECK_INTERVAL = 60  # Check every 60 seconds
TIMEFRAME = 15  # 15 minute window

# Store previous token data
token_history = {}

def get_pump_fun_tokens():
    """
    Get current pump.fun token data
    Replace with actual pump.fun data source
    """
    try:
        # Placeholder - needs actual pump.fun API
        response = requests.get(
            "https://api.mainnet-beta.solana.com",
            timeout=10
        )
        return []
    except:
        return []

def detect_volume_spike(token_address, current_volume):
    """
    Detect if volume spiked 200%+ in last 15 minutes
    """
    now = datetime.now()
    
    if token_address not in token_history:
        token_history[token_address] = {
            'volumes': [(now, current_volume)],
            'last_alert': None
        }
        return False
    
    # Clean old data (keep only last 15 minutes)
    token_history[token_address]['volumes'] = [
        (timestamp, vol) for timestamp, vol in token_history[token_address]['volumes']
        if now - timestamp < timedelta(minutes=TIMEFRAME)
    ]
    
    # Add current volume
    token_history[token_address]['volumes'].append((now, current_volume))
    
    # Check if we have data from 15 minutes ago
    if len(token_history[token_address]['volumes']) < 2:
        return False
    
    old_volume = token_history[token_address]['volumes'][0][1]
    
    if old_volume == 0:
        return False
    
    volume_ratio = current_volume / old_volume
    
    # Check if spike detected and not alerted recently
    if volume_ratio >= VOLUME_THRESHOLD:
        last_alert = token_history[token_address]['last_alert']
        if last_alert is None or (now - last_alert).seconds > 3600:
            token_history[token_address]['last_alert'] = now
            return True
    
    return False

def detect_liquidity_injection(token_address, current_liquidity, previous_liquidity):
    """
    Detect sudden liquidity additions
    """
    if previous_liquidity == 0:
        return False
    
    liquidity_increase = (current_liquidity - previous_liquidity) / previous_liquidity
    
    # 50%+ liquidity increase = injection
    if liquidity_increase >= 0.5:
        return True
    
    return False

def display_alerts(tokens_data):
    """
    Display detected signals
    tokens_data should be list of dicts with: address, symbol, volume, liquidity
    """
    import streamlit as st
    
    st.header("🚨 Live CTO Alerts")
    
    alerts = []
    
    for token in tokens_data:
        token_address = token.get('address')
        current_volume = token.get('volume', 0)
        
        # Check volume spike
        if detect_volume_spike(token_address, current_volume):
            volume_change = ((current_volume / token_history[token_address]['volumes'][0][1]) - 1) * 100
            alerts.append({
                'type': 'VOLUME SPIKE',
                'token': token.get('symbol', 'UNKNOWN'),
                'address': token_address,
                'change': f"+{volume_change:.0f}%",
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
    
    # Display alerts
    if alerts:
        for alert in alerts:
            st.error(f"""
⚡ {alert['type']} DETECTED

Token: {alert['token']}
Change: {alert['change']}
Time: {alert['timestamp']}

Chart: https://dexscreener.com/solana/{alert['address']}
            """)
    else:
        st.info("Monitoring for signals... No alerts yet.")
    
    return len(alerts)
```
