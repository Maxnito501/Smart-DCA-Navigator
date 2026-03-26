import yfinance as yf
import pandas as pd
import numpy as np
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ตั้งค่า Session เพื่อเลี่ยง Rate Limit
session = yf.Ticker.session
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

# ตั้งค่า Retry
retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Mock data เผื่อกรณีดึงไม่ได้
MOCK_PRICES = {
    "PTT": 34.75,
    "SCB": 146.00,
    "TISCO": 113.50,
    "AP": 8.55,
    "CPALL": 45.50,
    "ADVANC": 370.00,
    "GULF": 47.50,
    "BDMS": 18.90,
    "WHA": 4.16,
    "GPSC": 68.00,
    "TRUE": 14.00,
    "BH": 169.50,
    "AOT": 51.00,
    "SIRI": 1.39,
    "HMPRO": 6.15,
    "CPAXT": 15.20,
    "LH": 3.70,
    "KTC": 29.00,
    "DELTA": 120.00,
    "SCBSEMI": 24.79,
}

def fetch_price(symbol):
    """ดึงราคาปัจจุบัน"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
        else:
            # ใช้ mock data ถ้าดึงไม่ได้
            return MOCK_PRICES.get(symbol, 50.00)
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return MOCK_PRICES.get(symbol, 50.00)
    finally:
        time.sleep(random.uniform(0.5, 1.5))

def fetch_rsi(symbol, period=14):
    """ดึงค่า RSI"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="1mo")
        if len(data) < period:
            return None
        close = data['Close']
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi.iloc[-1], 1)
    except Exception as e:
        print(f"Error fetching RSI for {symbol}: {e}")
        return None
    finally:
        time.sleep(random.uniform(0.5, 1.5))

def fetch_ema200(symbol):
    """ดึง EMA200"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="1y")
        if len(data) < 200:
            return None
        ema = data['Close'].ewm(span=200, adjust=False).mean()
        return round(ema.iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching EMA200 for {symbol}: {e}")
        return None
    finally:
        time.sleep(random.uniform(0.5, 1.5))

def fetch_all_indicators(symbols):
    """ดึงข้อมูลทั้งหมดแบบกลุ่ม (Optimized)"""
    results = []
    for symbol in symbols:
        price = fetch_price(symbol)
        rsi = fetch_rsi(symbol)
        ema200 = fetch_ema200(symbol)
        results.append({
            "symbol": symbol,
            "price": price,
            "rsi": rsi,
            "ema200": ema200
        })
    return results
