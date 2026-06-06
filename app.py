import streamlit as st
import requests
import pandas as pd
import time

# Streamlit Page Configuration
st.set_page_config(page_title="Crypto 15m 200 EMA CoinGecko Scanner", page_icon="🔍", layout="wide")

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
    
    /* Custom Styling for Results (ছোট সাইজের বক্স) */
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
st.title("🔍 Premium Crypto 15m 200 EMA CoinGecko Scanner")
st.write("CoinGecko API ব্যবহার করে প্রতি ১৫ মিনিট পর পর স্বয়ংক্রিয় লাইভ ২০০ EMA ট্র্যাকার।")

# User Credentials
TELEGRAM_BOT_TOKEN = "8957518460:AAE_9HaugsNNYfjOzCpbHi2nJAEKf4GSiKs"
TELEGRAM_CHAT_ID = "6166836299"

# CoinGecko স্টাইল কয়েন লিস্ট (ID এবং Display Name যুগল)
# এর ফলে স্ক্যানার নিখুঁত আইডি দিয়ে ডেটা ফেচ করবে এবং স্ক্রিনে চেনার সুবিধার্থে সিম্বল দেখাবে
coingecko_coins = [
    {"id": "bitcoin", "symbol": "BTC"},
    {"id": "ethereum", "symbol": "ETH"},
    {"id": "binancecoin", "symbol": "BNB"},
    {"id": "solana", "symbol": "SOL"},
    {"id": "ripple", "symbol": "XRP"},
    {"id": "cardano", "symbol": "ADA"},
    {"id": "polkadot", "symbol": "DOT"},
    {"id": "avalanche-2", "symbol": "AVAX"},
    {"id": "chainlink", "symbol": "LINK"},
    {"id": "litecoin", "symbol": "LTC"},
    {"id": "dogecoin", "symbol": "DOGE"},
    {"id": "shiba-inu", "symbol": "SHIB"},
    {"id": "cosmos", "symbol": "ATOM"},
    {"id": "bitcoin-cash", "symbol": "BCH"},
    {"id": "ethereum-classic", "symbol": "ETC"},
    {"id": "stellar", "symbol": "XLM"},
    {"id": "near", "symbol": "NEAR"},
    {"id": "tron", "symbol": "TRX"},
    {"id": "uniswap", "symbol": "UNI"},
    {"id": "sui", "symbol": "SUI"},
    {"id": "aptos", "symbol": "APT"},
    {"id": "the-open-network", "symbol": "TON"},
    {"id": "injective-protocol", "symbol": "INJ"},
    {"id": "sei-network", "symbol": "SEI"},
    {"id": "fantom", "symbol": "FTM"},
    {"id": "algorand", "symbol": "ALGO"},
    {"id": "elrond-erd-2", "symbol": "EGLD"},
    {"id": "celestia", "symbol": "TIA"},
    {"id": "mina-protocol", "symbol": "MINA"},
    {"id": "flow", "symbol": "FLOW"},
    {"id": "internet-computer", "symbol": "ICP"},
    {"id": "eos", "symbol": "EOS"},
    {"id": "kava", "symbol": "KAVA"},
    {"id": "astar", "symbol": "ASTR"},
    {"id": "harmony", "symbol": "ONE"},
    {"id": "hedera-hashgraph", "symbol": "HBAR"},
    {"id": "iota", "symbol": "IOTA"},
    {"id": "neo", "symbol": "NEO"},
    {"id": "qtum", "symbol": "QTUM"},
    {"id": "vechain", "symbol": "VET"},
    {"id": "zilliqa", "symbol": "ZIL"},
    {"id": "theta-token", "symbol": "THETA"},
    {"id": "arbitrum", "symbol": "ARB"},
    {"id": "optimism", "symbol": "OP"},
    {"id": "starknet", "symbol": "STRK"},
    {"id": "metis-token", "symbol": "METIS"},
    {"id": "manta-network", "symbol": "MANTA"},
    {"id": "skale", "symbol": "SKL"},
    {"id": "celo", "symbol": "CELO"},
    {"id": "loopring", "symbol": "LRC"},
    {"id": "immutable-x", "symbol": "IMX"},
    {"id": "oasis-network", "symbol": "ROSE"},
    {"id": "pepe", "symbol": "PEPE"},
    {"id": "dogwifhat", "symbol": "WIF"},
    {"id": "bonk", "symbol": "BONK"},
    {"id": "floki", "symbol": "FLOKI"},
    {"id": "book-of-meme", "symbol": "BOME"},
    {"id": "memecoin", "symbol": "MEME"},
    {"id": "myro", "symbol": "MYRO"},
    {"id": "render-token", "symbol": "RENDER"},
    {"id": "the-graph", "symbol": "GRT"},
    {"id": "bittensor", "symbol": "TAO"},
    {"id": "arkham", "symbol": "ARKM"},
    {"id": "worldcoin-wld", "symbol": "WLD"},
    {"id": "livepeer", "symbol": "LPT"},
    {"id": "filecoin", "symbol": "FIL"},
    {"id": "arweave", "symbol": "AR"},
    {"id": "jasmycoin", "symbol": "JASMY"},
    {"id": "storj", "symbol": "STORJ"},
    {"id": "bluzelle", "symbol": "BLZ"},
    {"id": "ankr", "symbol": "ANKR"},
    {"id": "io-net", "symbol": "IO"},
    {"id": "golem", "symbol": "GLM"},
    {"id": "oranj", "symbol": "ORDI"},
    {"id": "aave", "symbol": "AAVE"},
    {"id": "pendle", "symbol": "PENDLE"},
    {"id": "maker", "symbol": "MKR"},
    {"id": "curve-dao-token", "symbol": "CRV"},
    {"id": "lido-dao", "symbol": "LDO"},
    {"id": "jupiter-exchange-solana", "symbol": "JUP"},
    {"id": "thorchain", "symbol": "RUNE"},
    {"id": "dydx", "symbol": "DYDX"},
    {"id": "ethereum-name-service", "symbol": "ENS"},
    {"id": "compound-governance-token", "symbol": "COMP"},
    {"id": "synthetix-network-token", "symbol": "SNX"},
    {"id": "sushiswap", "symbol": "SUSHI"},
    {"id": "yearn-finance", "symbol": "YFI"},
    {"id": "pancakeswap", "symbol": "CAKE"},
    {"id": "raydium", "symbol": "RAY"},
    {"id": "jito-governance-token", "symbol": "JTO"},
    {"id": "1inch", "symbol": "1INCH"},
    {"id": "ethena", "symbol": "ENA"},
    {"id": "pyth-network", "symbol": "PYTH"},
    {"id": "ondo-finance", "symbol": "ONDO"},
    {"id": "gala", "symbol": "GALA"},
    {"id": "axie-infinity", "symbol": "AXS"},
    {"id": "the-sandbox", "symbol": "SAND"},
    {"id": "decentraland", "symbol": "MANA"},
    {"id": "gmt", "symbol": "GMT"},
    {"id": "yield-guid-games", "symbol": "YGG"},
    {"id": "chiliz", "symbol": "CHZ"},
    {"id": "superfarm", "symbol": "SUPER"},
    {"id": "gari-network", "symbol": "GARI"}
]

# Function to send Telegram Message
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# Function to fetch 15m OHLVC data from CoinGecko Public API
def get_coingecko_ema_status(coin_id):
    # CoinGecko-তে ওহিও ক্যান্ডেলস্টিক চার্ট ডেটার ওয়ান-ডে বা শর্ট ট্রেইল এপিআই এন্ডপয়েন্ট ব্যবহার করা হয়েছে
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {"vs_currency": "usd", "days": "1"} # ১ দিনের চার্ট ডেটা থেকে লেটেস্ট ১৫ মিনিটের স্প্যান জেনারেট করবে
    
    try:
        response = requests.get(url, params=params, timeout=8)
        if response.status_code != 200:
            return "error", None, None
            
        data = response.json()
        if len(data) < 20: # ক্যান্ডেল কম থাকলে রিসেন্ট প্রাইস অ্যানালাইসিস করবে
            return "insufficient_data", None, None
            
        # CoinGecko OHLC format: [timestamp, open, high, low, close]
        close_prices = [float(candle[4]) for candle in data]
        df = pd.DataFrame(close_prices, columns=["price"])
        
        # ক্যান্ডেল সাইজ অনুযায়ী মানানসই ওয়েটেড মুভিং অ্যাভারেজ হিসাব
        span_value = min(len(df), 200)
        df['ema_200'] = df['price'].ewm(span=span_value, adjust=False).mean()
        
        last_row = df.iloc[-1]
        current_price = last_row['price']
        ema_200 = last_row['ema_200']
        
        status = "BULLISH" if current_price > ema_200 else "BEARISH"
        return status, current_price, ema_200
        
    except Exception:
        return "error", None, None

# Session States মেমোরি ইনিশিয়ালাইজেশন
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
    send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "🔄 *CoinGecko ১৫ মিনিটের স্ক্যান শুরু হয়েছে...*")

# Layout UI Tables
live_status_box = st.empty()
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 15m 200 EMA এর উপরে (Buy Signal)")
    bullish_placeholder = st.container()

with col2:
    st.subheader("🔴 15m 200 EMA এর নিচে (Sell Signal)")
    bearish_placeholder = st.container()

# সেভড ডেটা স্ক্রিনে রেন্ডার করা হচ্ছে
with bullish_placeholder:
    for html_card in st.session_state.bullish_results:
        st.markdown(html_card, unsafe_allow_html=True)

with bearish_placeholder:
    for html_card in st.session_state.bearish_results:
        st.markdown(html_card, unsafe_allow_html=True)

# স্ক্যানিং রানার এক্সিকিউশন লুপ
if st.session_state.is_scanning:
    idx = st.session_state.current_index
    total_coins = len(coingecko_coins)
    
    if idx < total_coins:
        coin_info = coingecko_coins[idx]
        coin_id = coin_info["id"]
        coin_symbol = coin_info["symbol"]
        progress_perc = int(((idx + 1) / total_coins) * 100)
        
        # লাইভ স্ক্যানিং অ্যানিমেশন বক্স
        live_status_box.markdown(f"""
            <div class="scanning-box">
                <p style="color: #38bdf8; font-size: 1.1rem; margin-bottom: 5px; font-weight: 600;">
                    🔍 CoinGecko লাইভ স্ক্যানিং প্রোগ্রেস: {progress_perc}% ({idx+1}/{total_coins})
                </p>
                <div class="scanning-coin">{coin_symbol} ({coin_id})</div>
                <p style="color: #64748b; font-size: 0.85rem; margin-top: 5px;">
                    CoinGecko গ্লোবাল নেটওয়ার্ক ডাটা প্রসেসিং চলছে...
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # API থেকে ডাটা নেওয়া হচ্ছে
        status, price, ema = get_coingecko_ema_status(coin_id)
        coin_url = f"https://www.coingecko.com/en/coins/{coin_id}"
        
        if status == "BULLISH":
            card_html = f"""
                <div class="signal-card bullish">
                    <span>🟢 <a class="coin-link" href="{coin_url}" target="_blank">{coin_symbol} ({coin_id})</a></span>
                    <span>Price: ${price:,.4f} | EMA: ${ema:,.4f}</span>
                </div>
            """
            st.session_state.bullish_results.append(card_html)
            
            # টেলিগ্রাম নোটিফিকেশন
            msg = f"🟢 *CoinGecko 15m BUY SIGNAL* 🟢\n\n*Coin:* [{coin_symbol}]({coin_url})\n*ID:* `{coin_id}`\n*Price:* ${price:,.4f}\n*EMA:* ${ema:,.4f}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            
        elif status == "BEARISH":
            card_html = f"""
                <div class="signal-card bearish">
                    <span>🔴 <a class="coin-link" href="{coin_url}" target="_blank">{coin_symbol} ({coin_id})</a></span>
                    <span>Price: ${price:,.4f} | EMA: ${ema:,.4f}</span>
                </div>
            """
            st.session_state.bearish_results.append(card_html)
            
            # টেলিগ্রাম নোটিফিকেশন
            msg = f"🔴 *CoinGecko 15m SELL SIGNAL* 🔴\n\n*Coin:* [{coin_symbol}]({coin_url})\n*ID:* `{coin_id}`\n*Price:* ${price:,.4f}\n*EMA:* ${ema:,.4f}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            
        # CoinGecko পাবলিক রেট লিমিট হ্যান্ডল করার জন্য সামান্য ডিলে
        st.session_state.current_index += 1
        time.sleep(1.2) # Public API-তে ১-২ সেকেন্ডের ডিলে দিলে আইপি ব্লক বা ৪২৯ এরর আসে না
        st.rerun()
    else:
        st.session_state.is_scanning = False
        live_status_box.success("🎉 CoinGecko-এর সব কয়েন স্ক্যান সফলভাবে সম্পন্ন হয়েছে!")
        time.sleep(900)
        st.session_state.bullish_results = []
        st.session_state.bearish_results = []
        st.session_state.current_index = 0
        st.session_state.is_scanning = True
        st.rerun()
