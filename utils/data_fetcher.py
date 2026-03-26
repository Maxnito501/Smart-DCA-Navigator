import yfinance as yf
import pandas as pd
import numpy as np
import time
import random

# ============================================
# Mock Data เผื่อกรณีดึงข้อมูลไม่ได้
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
# ฟังก์ชันดึงราคา
# ============================================
def fetch_price(symbol):
    """ดึงราคาปัจจุบัน (ใช้วิธีเดียวกับแอปเก่า)"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
        else:
            # ลองดึงแบบไม่มี .BK (เผื่อเป็นหุ้นต่างประเทศ)
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                return round(data['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
    
    # ถ้าดึงไม่ได้ ใช้ Mock Data
    return MOCK_PRICES.get(symbol, None)

# ============================================
# ฟังก์ชันดึง RSI
# ============================================
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
        time.sleep(random.uniform(0.3, 0.8))

def fetch_rsi_7(symbol):
    """ดึง RSI 7 วัน"""
    return fetch_rsi(symbol, period=7)

def fetch_rsi_21(symbol):
    """ดึง RSI 21 วัน"""
    return fetch_rsi(symbol, period=21)

# ============================================
# ฟังก์ชันดึง Moving Averages
# ============================================
def fetch_sma(symbol, period):
    """ดึง SMA (Simple Moving Average)"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period=f"{period+30}d")
        if len(data) < period:
            return None
        sma = data['Close'].rolling(window=period).mean()
        return round(sma.iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching SMA for {symbol}: {e}")
        return None
    finally:
        time.sleep(random.uniform(0.3, 0.8))

def fetch_ema(symbol, period):
    """ดึง EMA (Exponential Moving Average)"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period=f"{period+30}d")
        if len(data) < period:
            return None
        ema = data['Close'].ewm(span=period, adjust=False).mean()
        return round(ema.iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching EMA for {symbol}: {e}")
        return None
    finally:
        time.sleep(random.uniform(0.3, 0.8))

def fetch_ema200(symbol):
    """ดึง EMA200"""
    return fetch_ema(symbol, 200)

def fetch_sma20(symbol):
    """ดึง SMA20"""
    return fetch_sma(symbol, 20)

def fetch_sma50(symbol):
    """ดึง SMA50"""
    return fetch_sma(symbol, 50)

# ============================================
# ฟังก์ชันดึง MACD
# ============================================
def fetch_macd(symbol):
    """ดึงค่า MACD"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="3mo")
        if len(data) < 34:
            return None
        
        close = data['Close']
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return {
            'macd': round(macd_line.iloc[-1], 4),
            'signal': round(signal_line.iloc[-1], 4),
            'histogram': round(histogram.iloc[-1], 4)
        }
    except Exception as e:
        print(f"Error fetching MACD for {symbol}: {e}")
        return None
    finally:
        time.sleep(random.uniform(0.3, 0.8))

# ============================================
# ฟังก์ชันดึง Bollinger Bands
# ============================================
def fetch_bollinger(symbol):
    """ดึง Bollinger Bands"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="3mo")
        if len(data) < 20:
            return None
        
        close = data['Close']
        sma20 = close.rolling(window=20).mean()
        std20 = close.rolling(window=20).std()
        upper = sma20 + (std20 * 2)
        lower = sma20 - (std20 * 2)
        
        current_price = close.iloc[-1]
        bb_position = (current_price - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1]) if upper.iloc[-1] != lower.iloc[-1] else 0.5
        
        return {
            'upper': round(upper.iloc[-1], 2),
            'middle': round(sma20.iloc[-1], 2),
            'lower': round(lower.iloc[-1], 2),
            'position': round(bb_position * 100, 1)
        }
    except Exception as e:
        print(f"Error fetching Bollinger for {symbol}: {e}")
        return None
    finally:
        time.sleep(random.uniform(0.3, 0.8))

# ============================================
# ฟังก์ชันดึง Stochastic
# ============================================
def fetch_stochastic(symbol):
    """ดึง Stochastic Oscillator"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="1mo")
        if len(data) < 14:
            return None
        
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        highest_high = high.rolling(window=14).max()
        lowest_low = low.rolling(window=14).min()
        
        stoch_k = 100 * (close - lowest_low) / (highest_high - lowest_low)
        stoch_d = stoch_k.rolling(window=3).mean()
        
        return {
            'k': round(stoch_k.iloc[-1], 1),
            'd': round(stoch_d.iloc[-1], 1)
        }
    except Exception as e:
        print(f"Error fetching Stochastic for {symbol}: {e}")
        return None
    finally:
        time.sleep(random.uniform(0.3, 0.8))

# ============================================
# ฟังก์ชันดึง Volume Analysis
# ============================================
def fetch_volume_analysis(symbol):
    """วิเคราะห์ปริมาณการซื้อขาย"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        data = ticker.history(period="1mo")
        if len(data) < 20:
            return None
        
        volume_sma = data['Volume'].rolling(window=20).mean()
        volume_ratio = data['Volume'].iloc[-1] / volume_sma.iloc[-1] if volume_sma.iloc[-1] > 0 else 1
        
        return {
            'current_volume': int(data['Volume'].iloc[-1]),
            'avg_volume': int(volume_sma.iloc[-1]),
            'volume_ratio': round(volume_ratio, 2)
        }
    except Exception as e:
        print(f"Error fetching Volume for {symbol}: {e}")
        return None
    finally:
        time.sleep(random.uniform(0.3, 0.8))

# ============================================
# ฟังก์ชันดึงข้อมูลพื้นฐาน
# ============================================
def fetch_fundamental(symbol):
    """ดึงข้อมูลปัจจัยพื้นฐาน"""
    try:
        ticker = yf.Ticker(symbol + ".BK")
        info = ticker.info
        
        # ดึงข้อมูลที่ต้องการ
        pe = info.get('trailingPE')
        pb = info.get('priceToBook')
        roe = info.get('returnOnEquity')
        dividend_yield = info.get('dividendYield')
        
        # แปลง dividend yield
        if dividend_yield and dividend_yield < 1:
            dividend_yield = dividend_yield * 100
        
        return {
            'pe': round(pe, 2) if pe else None,
            'pb': round(pb, 2) if pb else None,
            'roe': round(roe * 100, 1) if roe else None,
            'dividend_yield': round(dividend_yield, 2) if dividend_yield else None
        }
    except Exception as e:
        print(f"Error fetching fundamental for {symbol}: {e}")
        return None
    finally:
        time.sleep(random.uniform(0.3, 0.8))

# ============================================
# ฟังก์ชันดึงข้อมูลทั้งหมด (รวมทุกตัว)
# ============================================
def fetch_all_indicators(symbols):
    """ดึงข้อมูลทั้งหมดสำหรับหุ้นหลายตัว"""
    results = []
    for symbol in symbols:
        result = {
            'symbol': symbol,
            'price': fetch_price(symbol),
            'rsi_14': fetch_rsi(symbol),
            'rsi_7': fetch_rsi_7(symbol),
            'rsi_21': fetch_rsi_21(symbol),
            'ema200': fetch_ema200(symbol),
            'sma20': fetch_sma20(symbol),
            'sma50': fetch_sma50(symbol),
            'macd': fetch_macd(symbol),
            'bollinger': fetch_bollinger(symbol),
            'stochastic': fetch_stochastic(symbol),
            'volume': fetch_volume_analysis(symbol),
            'fundamental': fetch_fundamental(symbol)
        }
        results.append(result)
        time.sleep(random.uniform(0.5, 1.0))
    
    return results
