import streamlit as st
import requests
import pandas as pd
import time

# Streamlit Page Configuration
st.set_page_config(page_title="Crypto 15m 200 EMA Scanner", page_icon="🔍", layout="wide")

# Advanced CSS for Luxury Look & Dynamic Glow Animations
st.markdown("""
    <style>
    /* Main Theme - Dark Luxury Background */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 100%);
        color: #f8fafc;
    }
    
    /* Glowing Title */
    h1 {
        color: #00d2ff !important;
        background: linear-gradient(to right, #00ffff, #0088ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 900 !important;
        text-shadow: 0px 0px 20px rgba(0, 255, 255, 0.3);
    }
    
    /* Sidebar Border & Dark Theme */
    [data-testid="stSidebar"] {
        background-color: #090d16 !important;
        border-right: 1px solid #1f2937;
    }
    
    /* Live Scanning Card Styling */
    .scanning-box {
        background: rgba(17, 24, 39, 0.85);
        border: 2px solid #38bdf8;
        box-shadow: 0px 0px 25px rgba(56, 189, 248, 0.4);
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin: 20px 0;
        animation: pulse 1.5s infinite alternate;
    }
    
    /* Glowing Scanning Coin */
    .scanning-coin {
        font-size: 3rem !important;
        font-weight: 800;
        color: #ff007f !important;
        text-shadow: 0 0 15px rgba(255, 0, 127, 0.6);
        letter-spacing: 2px;
    }
    
    /* Pulse Animation Logic */
    @keyframes pulse {
        0% { transform: scale(0.99); box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
        100% { transform: scale(1.01); box-shadow: 0 0 30px rgba(56, 189, 248, 0.6); }
    }
    
    /* Custom Styling for Results */
    .signal-card {
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .bullish {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #10b981;
    }
    .bearish {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        color: #ef4444;
    }
    .coin-link {
        color: #00d2ff;
        text-decoration: none;
    }
    .coin-link:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🔍 Premium Crypto 15m 200 EMA Live Scanner")
st.write("Binance API cloud network e direct run hobe. Auto-refresh optimization active.")

# User Credentials
TELEGRAM_BOT_TOKEN = "8957518460:AAE_9HaugsNNYfjOzCpbHi2nJAEKf4GSiKs"
TELEGRAM_CHAT_ID = "6166836299"

# Binance Pairs List (Filter kora list, jate speed high thake)
binance_symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", 
    "ADAUSDT", "DOTUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT", 
    "DOGEUSDT", "SHIBUSDT", "MATICUSDT", "ATOMUSDT", "BCHUSDT", 
    "ETCUSDT", "XLMUSDT", "NEARUSDT", "TRXUSDT", "UNIUSDT",
    "SUIUSDT", "APTUSDT", "TONUSDT", "INJUSDT", "SEIUSDT", 
    "FTMUSDT", "ALGOUSDT", "EGLDUSDT", "TIAUSDT", "MINAUSDT", 
    "FLOWUSDT", "ICPUSDT", "EOSUSDT", "KAVAUSDT", "ASTRUSDT", 
    "ONEUSDT", "HBARUSDT", "IOTAUSDT", "NEOUSDT", "QTUMUSDT", 
    "VETUSDT", "ZILUSDT", "WAVESUSDT", "THETAUSDT", "ARBUSDT", 
    "OPUSDT", "STRKUSDT", "METISUSDT", "MANTAUSDT", "SKLUSDT", 
    "CELOUSDT", "LRCUSDT", "IMXUSDT", "ROSEUSDT", "PEPEUSDT", 
    "WIFUSDT", "BONKUSDT", "FLOKIUSDT", "BOMEUSDT", "MEMEUSDT", 
    "MYROUSDT", "1000SATSUSDT", "TURBOUSDT", "PEOPLEUSDT", "NOTUSDT", 
    "POPCATUSDT", "BRETTUSDT", "MOGUSDT", "NEIROUSDT", "MOODENGUSDT", 
    "GOATUSDT", "PNUTUSDT", "ACTUSDT", "FETUSDT", "GRTUSDT", 
    "TAOUSDT", "ARKMUSDT", "WLDUSDT", "LPTUSDT", "FILUSDT", 
    "ARUSDT", "JASMYUSDT", "STORJUSDT", "BLZUSDT", "ANKRUSDT", 
    "ORDIUSDT", "AAVEUSDT", "PENDLEUSDT", "MKRUSDT", "CRVUSDT", 
    "LDOUSDT", "JUPUSDT", "RUNEUSDT", "DYDXUSDT", "ENSUSDT", 
    "SNXUSDT", "SUSHIUSDT", "YFIUSDT", "CAKEUSDT", "RAYUSDT", 
    "JTOUSDT", "1INCHUSDT", "ENAUSDT", "PYTHUSDT", "ONDOUSDT", 
    "GALAUSDT", "AXSUSDT", "SANDUSDT", "MANAUSDT", "PIXELUSDT", 
    "YGGUSDT", "CHZUSDT", "SUPERUSDT", "BIGTIMEUSDT", "TOKENUSDT", 
    "VANRYUSDT", "ZECUSDT", "XMRUSDT", "DASHUSDT", "ZENUSDT", 
    "IOTXUSDT", "HOTUSDT", "BATUSDT", "WOOUSDT", "GMTUSDT", "IDUSDT"
]

# Function to send Telegram Message
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        pass

# Function to fetch data from Binance and calculate 15m 200 EMA
def get_binance_ema_status(symbol):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": "15m", "limit": "300"}
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            return None, None, None
        data = response.json()
        if len(data) < 200:
            return None, None, None
            
        close_prices = [float(candle[4]) for candle in data]
        df = pd.DataFrame(close_prices, columns=["price"])
        df['ema_200'] = df['price'].ewm(span=200, adjust=False).mean()
        
        last_row = df.iloc[-1]
        return "BULLISH" if last_row['price'] > last_row['ema_200'] else "BEARISH", last_row['price'], last_row['ema_200']
    except:
        return None, None, None

# Initialize Session States for permanent UI display
if 'bullish_list' not in st.session_state:
    st.session_state.bullish_list = []
if 'bearish_list' not in st.session_state:
    st.session_state.bearish_list = []

# Sidebar Controls
st.sidebar.header("⚙️ Control Panel")
scan_now = st.sidebar.button("🚀 Start Scan")

# Automatic 15-minute refresh using Streamlit configuration
if st.sidebar.checkbox("🔄 Enable Auto 15m Loop", value=False):
    st.sidebar.caption("Auto-refresh active. Dashboard will refresh every 15 mins.")
    time_delay = 900
else:
    time_delay = None

# UI Containers setup
live_status_box = st.empty()
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 15m 200 EMA Up (Buy Signal)")
    bullish_ui = st.container()

with col2:
    st.subheader("🔴 15m 200 EMA Down (Sell Signal)")
    bearish_ui = st.container()

# Render previous session results instantly so screen is never empty
for coin in st.session_state.bullish_list:
    bullish_ui.markdown(coin, unsafe_allow_html=True)
for coin in st.session_state.bearish_list:
    bearish_ui.markdown(coin, unsafe_allow_html=True)

# Main Trigger Loop
if scan_now or time_delay:
    # Clear active lists for fresh calculation
    st.session_state.bullish_list = []
    st.session_state.bearish_list = []
    bullish_ui.empty()
    bearish_ui.empty()
    
    total_coins = len(binance_symbols)
    send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "🔄 *15m 200 EMA Live Scan Started!*")
    
    for i, symbol in enumerate(binance_symbols):
        progress_perc = int(((i + 1) / total_coins) * 100)
        
        # Pop-up animation logic
        live_status_box.markdown(f"""
            <div class="scanning-box">
                <p style="color: #38bdf8; font-size: 1.2rem; margin-bottom: 5px; font-weight: 600;">
                    🔍 LIVE SCANNING: {progress_perc}% ({i+1}/{total_coins})
                </p>
                <div class="scanning-coin">{symbol}</div>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">
                    Binance Data Processing Network Live...
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        status, price, ema = get_binance_ema_status(symbol)
        coin_url = f"https://www.binance.com/en/trade/{symbol.replace('USDT', '_USDT')}"
        
        if status == "BULLISH":
            card_html = f"""
                <div class="signal-card bullish">
                    <span>🟢 <a class="coin-link" href="{coin_url}" target="_blank">{symbol}</a></span>
                    <span>Price: ${price:,.4f} | EMA: ${ema:,.4f}</span>
                </div>
            """
            st.session_state.bullish_list.append(card_html)
            bullish_ui.markdown(card_html, unsafe_allow_html=True)
            
            # Instant Telegram Alert
            msg = f"🟢 *15m BUY SIGNAL* 🟢\n\n*Coin:* [{symbol}]({coin_url})\n*Price:* ${price:,.4f}\n*200 EMA:* ${ema:,.4f}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            
        elif status == "BEARISH":
            card_html = f"""
                <div class="signal-card bearish">
                    <span>🔴 <a class="coin-link" href="{coin_url}" target="_blank">{symbol}</a></span>
                    <span>Price: ${price:,.4f} | EMA: ${ema:,.4f}</span>
                </div>
            """
            st.session_state.bearish_list.append(card_html)
            bearish_ui.markdown(card_html, unsafe_allow_html=True)
            
            # Instant Telegram Alert
            msg = f"🔴 *15m SELL SIGNAL* 🔴\n\n*Coin:* [{symbol}]({coin_url})\n*Price:* ${price:,.4f}\n*200 EMA:* ${ema:,.4f}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            
        time.sleep(0.05) # Superfast response handling
        
    live_status_box.success("🎉 Scan Completed Successfully!")
    
    if time_delay:
        time.sleep(time_delay)
        st.rerun()
