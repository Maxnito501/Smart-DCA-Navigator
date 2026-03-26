import yfinance as yf
import pandas as pd
import numpy as np
import time
import random

def fetch_price(symbol):
    """ดึงราคาปัจจุบัน"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
        time.sleep(random.uniform(0.5, 1.5))
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
    return None

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
        time.sleep(random.uniform(0.5, 1.5))
        return round(rsi.iloc[-1], 1)
    except:
        pass
    return None

def fetch_ema200(symbol):
    """ดึง EMA200"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="1y")
        if len(data) < 200:
            return None
        ema = data['Close'].ewm(span=200, adjust=False).mean()
        time.sleep(random.uniform(0.5, 1.5))
        return round(ema.iloc[-1], 2)
    except:
        pass
    return None
