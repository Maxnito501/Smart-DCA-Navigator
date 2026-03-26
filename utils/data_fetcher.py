import yfinance as yf
import pandas as pd
import numpy as np
import time
import random
import requests_cache
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ============================================
# เสาหลักที่ 1: ปลอมตัวเป็น Browser
# ============================================
session = requests_cache.CachedSession('yfinance_cache', expire_after=3600)  # เสาหลักที่ 2: Caching
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

# ตั้งค่า Retry
retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# ให้ yfinance ใช้ session ที่ตั้งค่าไว้
yf.set_tz_cache_location('yfinance_tz_cache')

def fetch_batch_prices(symbols):
    """
    เสาหลักที่ 4: ดึงแบบกลุ่ม (Bulk Download)
    ดึงราคาหุ้นหลายตัวในครั้งเดียว
    """
    try:
        # เติม .BK สำหรับหุ้นไทย
        tickers = [s + ".BK" for s in symbols]
        data = yf.download(tickers, period="1d", group_by='ticker', session=session)
        
        prices = {}
        for symbol in symbols:
            ticker = symbol + ".BK"
            if ticker in data:
                prices[symbol] = round(data[ticker]['Close'].iloc[-1], 2)
            else:
                prices[symbol] = None
        return prices
    except Exception as e:
        print(f"Batch fetch error: {e}")
        return {s: None for s in symbols}

def fetch_price(symbol):
    """ดึงราคาหุ้นตัวเดียว (ใช้ batch ดีกว่า)"""
    return fetch_batch_prices([symbol]).get(symbol)

def fetch_batch_rsi(symbols, period=14):
    """
    ดึง RSI แบบกลุ่ม (ทีละตัว เนื่องจาก RSI ต้องคำนวณแยก)
    เสาหลักที่ 3: สุ่มเวลาหน่วง
    """
    results = {}
    for i, symbol in enumerate(symbols):
        try:
            ticker = symbol + ".BK"
            data = yf.download(ticker, period="1mo", session=session)
            if len(data) < period:
                results[symbol] = None
            else:
                close = data['Close']
                delta = close.diff()
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                avg_gain = gain.rolling(window=period).mean()
                avg_loss = loss.rolling(window=period).mean()
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                results[symbol] = round(rsi.iloc[-1], 1)
        except Exception as e:
            results[symbol] = None
        
        # เสาหลักที่ 3: หน่วงเวลาและสุ่ม
        time.sleep(random.uniform(1, 3))
    
    return results

def fetch_rsi(symbol, period=14):
    """ดึง RSI ตัวเดียว"""
    return fetch_batch_rsi([symbol], period).get(symbol)

def fetch_batch_ema200(symbols):
    """ดึง EMA200 แบบกลุ่ม"""
    results = {}
    for i, symbol in enumerate(symbols):
        try:
            ticker = symbol + ".BK"
            data = yf.download(ticker, period="1y", session=session)
            if len(data) < 200:
                results[symbol] = None
            else:
                ema = data['Close'].ewm(span=200, adjust=False).mean()
                results[symbol] = round(ema.iloc[-1], 2)
        except Exception as e:
            results[symbol] = None
        
        # หน่วงเวลา
        time.sleep(random.uniform(1, 2))
    
    return results

def fetch_ema200(symbol):
    """ดึง EMA200 ตัวเดียว"""
    return fetch_batch_ema200([symbol]).get(symbol)

def fetch_all_indicators(symbols):
    """
    ดึง Indicator ทั้งหมดแบบกลุ่ม (Optimized)
    """
    prices = fetch_batch_prices(symbols)
    rsi_dict = fetch_batch_rsi(symbols)
    ema_dict = fetch_batch_ema200(symbols)
    
    results = []
    for symbol in symbols:
        results.append({
            "symbol": symbol,
            "price": prices.get(symbol),
            "rsi": rsi_dict.get(symbol),
            "ema200": ema_dict.get(symbol)
        })
    return results
