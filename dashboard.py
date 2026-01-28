import streamlit as st
import requests
import os
import time

# --- INITIAL CONFIG (Must be first) ---
st.set_page_config(
    page_title="CTO Terminal 💻",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENVIRONMENT & RPC SETUP ---
RPC_URL = os.getenv("SOLANA_RPC_URL")

def get_current_slot():
    if not RPC_URL:
        return "RPC URL MISSING"
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getSlot", "params": []}
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10).json()
        return response.get("result", "Error")
    except Exception as e:
        return f"RPC Error"

# --- CUSTOM CSS ---
st.markdown("""
<style>
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Neon glow and premium typography */
    h1, h2, h3 {
        color: #00D4FF !important;
        text-shadow: 0 0 10px #00D4FF80;
        font-family: 'Segoe UI', sans-serif;
    }

    /* KPI Card styling */
    div[data-testid="metric-container"] {
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        background-color: #111827;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.15);
    }

    /* Hero Banner Styling */
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

    .block-container { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# --- UI COMPONENTS ---

# 1. Hero Banner
st.markdown(
    """
    <div class="hero-banner">
        <h2 style='margin:0; color:#00D4FF;'>CTO Terminal – Front-Run Solana Comebacks</h2>
        <p style='color:#CBD5E1; font-size:1.1rem;'>Real-time detection of liquidity injections, volume spikes & wallet clusters on pump.fun</p>
        <code style='color:#00D4FF;'>V1 in development | Building live for @pumpdotfun Hackathon</code>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("CTO Terminal")
    st.info("Monitoring for:\n- Sudden volume spikes\n- Liquidity injections\n- Early CTO signals")
    refresh_rate = st.slider("Refresh interval (seconds)", 1, 30, 5)
    st.markdown("---")
    st.markdown("Follow progress: [@CTOTERMINAL](https://x.com/CTOTERMINAL)")

if not RPC_URL:
    st.error("SOLANA_RPC_URL variable is not set in Railway Settings.")
    st.stop()

# --- MAIN LOOP ---
placeholder = st.empty()

while True:
    with placeholder.container():
        slot = get_current_slot()
        
        # 2. Upgrade Metrics to 3 Colorful Cards
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric(label="Current Solana Slot", value=slot, help="Latest confirmed slot from RPC")
        with kpi2:
            st.metric(label="Refresh Rate", value=f"{refresh_rate}s", delta="Live", delta_color="normal")
        with kpi3:
            st.metric(label="Detected Signals", value="0", delta="Awaiting CTOs", delta_color="inverse")

        # 3. Styled Alerts Section
        st.subheader("Live Token Volume & CTO Alerts 🔥")
        st.markdown(
            """
            <div class="alert-box">
                <p style='margin:0; font-weight:bold; color:#00D4FF;'>System Status: Scanning pump.fun...</p>
                <p style='margin:0; font-size:0.9rem; color:#94a3b8;'>
                Tuning detection for liquidity adds, volume spikes (200%+), and fresh wallet clusters. 
                First CTO will appear here with: Token mint | Spike % | Liq amount | Cluster count.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Styled Dataframe
        st.markdown("**Sample Monitoring (Demo Mode)**")
        sample_data = {
            "Token": ["EXAMPLE1", "EXAMPLE2"],
            "5min Volume": [45000, 12000],
            "Liq Added": [True, False],
            "CTO Score": ["High", "Medium"]
        }
        st.dataframe(
            sample_data,
            use_container_width=True,
            column_config={
                "Token": st.column_config.TextColumn("Token"),
                "5min Volume": st.column_config.NumberColumn("Volume ($)", format="$%d"),
                "Liq Added": st.column_config.CheckboxColumn("Liq Injected"),
                "CTO Score": st.column_config.TextColumn("Score")
            }
        )
        
        # 4. Footer (Inside loop to keep it at the bottom during refresh)
        st.markdown("---")
        st.caption("CTO Terminal 💻 | Solo build from Ibadan 🇳🇬 | Follow @CTOTERMINAL for updates")

    time.sleep(refresh_rate)
