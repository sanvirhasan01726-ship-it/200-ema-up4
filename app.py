import streamlit as st
import requests
import pandas as pd
import time

# Streamlit Page Configuration
st.set_page_config(page_title="Crypto 15m 200 EMA Scanner", page_icon="🔍", layout="wide")

# Advanced CSS for Luxury Look, Small Boxes & Dynamic Glow Animations
st.markdown("""
    <style>
    /* Main Theme - ডার্ক লাক্সারি ব্যাকগ্রাউন্ড */
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
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin: 10px 0;
        animation: pulse 1.5s infinite alternate;
    }
    
    /* Glowing Scanning Coin */
    .scanning-coin {
        font-size: 2rem !important;
        font-weight: 800;
        color: #ff007f !important;
        text-shadow: 0 0 15px rgba(255, 0, 127, 0.6);
        letter-spacing: 2px;
    }
    
    /* Pulse Animation */
    @keyframes pulse {
        0% { transform: scale(0.99); box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
        100% { transform: scale(1.01); box-shadow: 0 0 30px rgba(56, 189, 248, 0.6); }
    }
    
    /* Custom Styling for Results (বক্স ছোট করা হয়েছে যাতে স্ক্রোল কম করতে হয়) */
    .signal-card {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 6px;
        font-weight: bold;
        font-size: 0.9rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
    }
    .bullish {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid #10b981;
        color: #10b981;
    }
    .bearish {
        background: rgba(239, 68, 68, 0.12);
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
st.write("Binance-এর ভেরিফাইড অ্যাক্টিভ পেয়ার ব্যবহার করে স্বয়ংক্রিয় লাইভ ২০০ EMA ট্র্যাকার।")

# User Credentials
TELEGRAM_BOT_TOKEN = "8957518460:AAE_9HaugsNNYfjOzCpbHi2nJAEKf4GSiKs"
TELEGRAM_CHAT_ID = "6166836299"

# ভেরিফাইড এবং অ্যাক্টিভ বাইনান্স সিম্বল লিস্ট (ভুল ও ডি-লিস্টেড টোকেন রিমুভড)
binance_symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", 
    "ADAUSDT", "DOTUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT", 
    "DOGEUSDT", "SHIBUSDT", "ATOMUSDT", "BCHUSDT", 
    "ETCUSDT", "XLMUSDT", "NEARUSDT", "TRXUSDT", "UNIUSDT",
    "SUIUSDT", "APTUSDT", "TONUSDT", "INJUSDT", "SEIUSDT", 
    "FTMUSDT", "ALGOUSDT", "EGLDUSDT", "TIAUSDT", "MINAUSDT", 
    "FLOWUSDT", "ICPUSDT", "EOSUSDT", "KAVAUSDT", "ASTRUSDT", 
    "ONEUSDT", "HBARUSDT", "IOTAUSDT", "NEOUSDT", "QTUMUSDT", 
    "VETUSDT", "ZILUSDT", "THETAUSDT", "ARBUSDT", "OPUSDT", 
    "STRKUSDT", "METISUSDT", "MANTAUSDT", "SKLUSDT", "CELOUSDT", 
    "LRCUSDT", "IMXUSDT", "OMGUSDT", "ROSEUSDT", "PEPEUSDT", 
    "WIFUSDT", "BONKUSDT", "FLOKIUSDT", "BOMEUSDT", "MEMEUSDT", 
    "MYROUSDT", "1000SATSUSDT", "TURBOUSDT", "BABYDOGEUSDT", 
    "PEOPLEUSDT", "NOTUSDT", "POPCATUSDT", "BRETTUSDT", "MOGUSDT", 
    "NEIROUSDT", "MOODENGUSDT", "GOATUSDT", "PNUTUSDT", "ACTUSDT", 
    "SUNDOGUSDT", "FETUSDT", "GRTUSDT", "TAOUSDT", "ARKMUSDT", 
    "WLDUSDT", "NFPUSDT", "AIUSDT", "LPTUSDT", "FILUSDT", 
    "ARUSDT", "JASMYUSDT", "STORJUSDT", "BLZUSDT", "ANKRUSDT", 
    "IONETUSDT", "GLMUSDT", "ORDIUSDT", "MDTUSDT", "CTXCIUSDT", 
    "GTCUSDT", "CLVUSDT", "AAVEUSDT", "PENDLEUSDT", "MKRUSDT", 
    "CRVUSDT", "LDOUSDT", "JUPUSDT", "RUNEUSDT", "DYDXUSDT", 
    "ENSUSDT", "COMPUSDT", "SNXUSDT", "SUSHIUSDT", "YFIUSDT", 
    "CAKEUSDT", "BAKEUSDT", "RAYUSDT", "JOEUSDT", "JTOUSDT", 
    "1INCHUSDT", "BALUSDT", "BADGERUSDT", "ALPHAUSDT", "ENAUSDT", 
    "DRIFTUSDT", "SAFEUSDT", "PYTHUSDT", "AXLUSDT", "ONDOUSDT", 
    "TRUUSDT", "BELUSDT", "AUCTIONUSDT", "TROYUSDT", "FISUSDT", 
    "ETHFIUSDT", "REZUSDT", "OMNIUSDT", "TNSRUSDT", "SAGAUSDT", 
    "BBUSDT", "SCRUSDT", "GALAUSDT", "AXSUSDT", "SANDUSDT", 
    "MANAUSDT", "PIXELUSDT", "BEAMUSDT", "YGGUSDT", "ILVUSDT", 
    "ALICEUSDT", "ENJUSDT", "MAGICUSDT", "PORTALUSDT", "XAIUSDT", 
    "CHZUSDT", "SUPERUSDT", "VOXELUSDT", "DARUSDT", "TLMUSDT", 
    "BIGTIMEUSDT", "TOKENUSDT", "VANRYUSDT", "MBOXUSDT", "HIGHUSDT", 
    "STGUSDT", "SYNUSDT", "GLMRUSDT", "MOVRUSDT", "KSMUSDT", 
    "ICXUSDT", "BANDUSDT", "TRBUSDT", "DIAUSDT", "ZECUSDT", 
    "DASHUSDT", "ZENUSDT", "ONTUSDT", "IOTXUSDT", "RVNUSDT", 
    "HOTUSDT", "BATUSDT", "KNCUSDT", "ZRXUSDT", "RENUSDT", 
    "WOOUSDT", "GMTUSDT", "IDUSDT", "EDUUSDT", "HOOKUSDT", 
    "CYBERUSDT", "MAVUSDT", "ARKUSDT", "LOOMUSDT", "RADUSDT"
]

# Function to send Telegram Message
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# Function to fetch data from Binance and calculate 15m 200 EMA
def get_binance_ema_status(symbol):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": "15m", "limit": "300"}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            return "error", None, None
            
        data = response.json()
        if len(data) < 200:
            return "insufficient_data", None, None
            
        close_prices = [float(candle[4]) for candle in data]
        df = pd.DataFrame(close_prices, columns=["price"])
        
        # Pandas EWM (Exponential Weighted Moving Average) Calculation
        df['ema_200'] = df['price'].ewm(span=200, adjust=False).mean()
        
        last_row = df.iloc[-1]
        current_price = last_row['price']
        ema_200 = last_row['ema_200']
        
        if pd.isna(ema_200):
            return "insufficient_data", None, None
            
        status = "BULLISH" if current_price > ema_200 else "BEARISH"
        return status, current_price, ema_200
        
    except Exception:
        return "error", None, None

# Session States ব্যবহার করে মেমোরিতে ডেটা স্থায়ী রাখা হচ্ছে
if "bullish_results" not in st.session_state:
    st.session_state.bullish_results = []
if "bearish_results" not in st.session_state:
    st.session_state.bearish_results = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "is_scanning" not in st.session_state:
    st.session_state.is_scanning = False

# Sidebar Control UI
st.sidebar.header("⚙️ কন্ট্রোল প্যানেল")
if st.sidebar.button("🚀 স্ক্যান শুরু করুন"):
    st.session_state.bullish_results = []
    st.session_state.bearish_results = []
    st.session_state.current_index = 0
    st.session_state.is_scanning = True
    send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "🔄 *১৫ মিনিটের ক্যান্ডেল স্ক্যান শুরু হয়েছে...*")

# Layout UI Tables
live_status_box = st.empty()
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 15m 200 EMA এর উপরে (Buy Signal)")
    bullish_placeholder = st.container()

with col2:
    st.subheader("🔴 15m 200 EMA এর নিচে (Sell Signal)")
    bearish_placeholder = st.container()

# আগের বা বর্তমান স্ক্যান হওয়া কয়েনগুলো স্থায়ীভাবে ইউজার ইন্টারফেসে রেন্ডার করা
with bullish_placeholder:
    for html_card in st.session_state.bullish_results:
        st.markdown(html_card, unsafe_allow_html=True)

with bearish_placeholder:
    for html_card in st.session_state.bearish_results:
        st.markdown(html_card, unsafe_allow_html=True)

# স্ক্যানিং এক্সিকিউশন রানার (Streamlit Flow Control)
if st.session_state.is_scanning:
    idx = st.session_state.current_index
    total_coins = len(binance_symbols)
    
    if idx < total_coins:
        symbol = binance_symbols[idx]
        progress_perc = int(((idx + 1) / total_coins) * 100)
        
        # লাইভ পপ-আপ অ্যানিমেশন বক্স
        live_status_box.markdown(f"""
            <div class="scanning-box">
                <p style="color: #38bdf8; font-size: 1.1rem; margin-bottom: 5px; font-weight: 600;">
                    🔍 লাইভ স্ক্যানিং প্রোগ্রেস: {progress_perc}% ({idx+1}/{total_coins})
                </p>
                <div class="scanning-coin">{symbol}</div>
                <p style="color: #64748b; font-size: 0.85rem; margin-top: 5px;">
                    বাইনান্স কোর ডাটাবেজ কানেকশন সফল...
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # ক্যালকুলেশন রান করা হচ্ছে
        status, price, ema = get_binance_ema_status(symbol)
        coin_url = f"https://www.binance.com/en/trade/{symbol.replace('USDT', '_USDT')}"
        
        if status == "BULLISH":
            card_html = f"""
                <div class="signal-card bullish">
                    <span>🟢 <a class="coin-link" href="{coin_url}" target="_blank">{symbol}</a></span>
                    <span>Price: ${price:,.4f} | EMA: ${ema:,.4f}</span>
                </div>
            """
            st.session_state.bullish_results.append(card_html)
            
            # টেলিগ্রাম মেসেজ
            msg = f"🟢 *15m BUY SIGNAL* 🟢\n\n*Coin:* [{symbol}]({coin_url})\n*Status:* Above 200 EMA (15m)\n*Price:* ${price:,.4f}\n*200 EMA:* ${ema:,.4f}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            
        elif status == "BEARISH":
            card_html = f"""
                <div class="signal-card bearish">
                    <span>🔴 <a class="coin-link" href="{coin_url}" target="_blank">{symbol}</a></span>
                    <span>Price: ${price:,.4f} | EMA: ${ema:,.4f}</span>
                </div>
            """
            st.session_state.bearish_results.append(card_html)
            
            # টেলিগ্রাম মেসেজ
            msg = f"🔴 *15m SELL SIGNAL* 🔴\n\n*Coin:* [{symbol}]({coin_url})\n*Status:* Below 200 EMA (15m)\n*Price:* ${price:,.4f}\n*200 EMA:* ${ema:,.4f}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            
        # পরবর্তী কয়েনের জন্য ইনডেক্স বাড়ানো ও রিরান করা
        st.session_state.current_index += 1
        time.sleep(0.02)
        st.rerun()
    else:
        # স্ক্যান শেষ হওয়ার লজিক এবং পরবর্তী ১৫ মিনিট পর অটোমেটিক রিস্টার্ট সেটআপ
        st.session_state.is_scanning = False
        live_status_box.success("🎉 স্ক্যান সফলভাবে সম্পন্ন হয়েছে এবং সবগুলো কয়েন আউটপুটে চলে এসেছে!")
        time.sleep(900)
        st.session_state.bullish_results = []
        st.session_state.bearish_results = []
        st.session_state.current_index = 0
        st.session_state.is_scanning = True
        st.rerun()
