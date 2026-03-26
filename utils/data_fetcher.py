import yfinance as yf 
import pandas as pd 
import numpy as np 
 
def fetch_price(symbol, period="1d"): 
    try: 
        ticker = yf.Ticker(symbol) 
        data = ticker.history(period=period) 
        if not data.empty: 
            return data['Close'].iloc[-1] 
    except: 
        pass 
    return None 
 
def fetch_rsi(symbol, period=14): 
    try: 
        ticker = yf.Ticker(symbol) 
        data = ticker.history(period="1mo") 
            return None 
        close = data['Close'] 
        delta = close.diff() 
        gain = delta.where(delta , 0) 
        avg_gain = gain.rolling(window=period).mean() 
        avg_loss = loss.rolling(window=period).mean() 
        rs = avg_gain / avg_loss 
        rsi = 100 - (100 / (1 + rs)) 
        return round(rsi.iloc[-1], 1) 
    except: 
        pass 
    return None 
 
def fetch_historical(symbol, period="5y"): 
    try: 
        ticker = yf.Ticker(symbol) 
        data = ticker.history(period=period) 
        return data 
    except: 
        pass 
    return pd.DataFrame() 
 
def fetch_indicators(symbol): 
    price = fetch_price(symbol) 
    rsi = fetch_rsi(symbol) 
    return {"price": price, "rsi": rsi} 
