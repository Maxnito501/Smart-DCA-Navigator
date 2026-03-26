import yfinance as yf
import pandas as pd
import numpy as np
import time
import random
import requests

# ============================================
# ตั้งค่า Session + User-Agent (สำคัญมาก)
# ============================================
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

# ตั้งค่า yfinance ให้ใช้ session นี้
yf.set_tz_cache_location('yfinance_tz_cache')

# ============================================
# Mock Data เผื่อกรณีดึงไม่ได้
# ============================================
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

# ============================================
# ฟังก์ชันดึงข้อมูล (พร้อม Random Delay)
# ============================================
def random_delay():
    """หน่วงเวลาแบบสุ่ม ป้องกัน Rate Limit"""
    time.sleep(random.uniform(0.5, 1.5))

def fetch_price(symbol):
    """ดึงราคาปัจจุบัน"""
    try:
        random_delay()
        ticker = yf.Ticker(symbol + ".BK", session=session)
        data = ticker.history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
    
    return MOCK_PRICES.get(symbol, None)

def fetch_price_batch(symbols):
    """ดึงราคาหลายตัวพร้อมกัน (Batch)"""
    try:
        random_delay()
        tickers = [s + ".BK" for s in symbols]
        data = yf.download(tickers, period="1d", group_by='ticker', session=session)
        
        prices = {}
        for symbol in symbols:
            ticker = symbol + ".BK"
            if ticker in data:
                prices[symbol] = round(data[ticker]['Close'].iloc[-1], 2)
            else:
                prices[symbol] = MOCK_PRICES.get(symbol, None)
        return prices
    except Exception as e:
        print(f"Batch fetch error: {e}")
        return {s: MOCK_PRICES.get(s, None) for s in symbols}

def fetch_rsi(symbol, period=14):
    """ดึงค่า RSI"""
    try:
        random_delay()
        ticker = yf.Ticker(symbol + ".BK", session=session)
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

def fetch_ema200(symbol):
    """ดึง EMA200"""
    try:
        random_delay()
        ticker = yf.Ticker(symbol + ".BK", session=session)
        data = ticker.history(period="1y")
        if len(data) < 200:
            return None
        ema = data['Close'].ewm(span=200, adjust=False).mean()
        return round(ema.iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching EMA200 for {symbol}: {e}")
        return None

def fetch_all_indicators(symbols):
    """ดึงข้อมูลทั้งหมดแบบกลุ่ม (ใช้ Batch)"""
    prices = fetch_price_batch(symbols)
    
    results = []
    for symbol in symbols:
        result = {
            'symbol': symbol,
            'price': prices.get(symbol),
            'rsi_14': fetch_rsi(symbol),
            'ema200': fetch_ema200(symbol),
        }
        results.append(result)
    
    return results
