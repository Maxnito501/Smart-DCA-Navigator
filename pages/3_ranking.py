import streamlit as st 
import pandas as pd 
import numpy as np 
import sys 
import os 
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from utils.config import get_watchlist 
 
st.set_page_config(layout="wide") 
 
st.title("📊 Ranking หุ้น/กองทุนน่าเข้าซื้อ") 
st.markdown("จัดลำดับตามกลยุทธ์ Core (ถือยาว) และ Satellite (เล่นรอบ)") 
 
@st.cache_data 
def load_core(): 
    return pd.read_csv("data/watchlist_core.csv") 
 
@st.cache_data 
def load_satellite(): 
    return pd.read_csv("data/watchlist_satellite.csv") 
 
core = load_core() 
satellite = load_satellite() 
 
def generate_ranking_data(stocks, mode="core"): 
    np.random.seed(42) 
    data = [] 
    for stock in stocks[:10]: 
        rsi = np.random.uniform(20, 80) 
        price = np.random.uniform(10, 200) 
        ema200 = price * np.random.uniform(0.85, 1.15) 
        if mode == "core": 
            score = 0 
                score += 30 
                score += 20 
                score += 25 
            score += np.random.uniform(0, 20) 
        else: 
            score = 0 
                score += 25 
            stoch = np.random.uniform(10, 90) 
                score += 25 
            macd = np.random.choice(["ตัดขึ้น", "ตัดลง"]) 
            if macd == "ตัดขึ้น": 
                score += 25 
            score += np.random.uniform(0, 15) 
            compare_ema = "-" 
        data.append({ 
            "หุ้น": stock, 
            "ราคา": round(price, 2), 
            "RSI": round(rsi, 1), 
            "EMA200": round(ema200, 2), 
            "เทียบ EMA200": compare_ema, 
            "คะแนน": int(score) 
        }) 
    df = pd.DataFrame(data) 
    return df.sort_values("คะแนน", ascending=False).reset_index(drop=True) 
 
st.info("📡 กำลังจำลองข้อมูล (ของจริงจะดึงจาก yfinance/SET API)") 
 
tab1, tab2 = st.tabs(["🏆 Core (ถือยาว) — เน้นราคาถูก", "🚀 Satellite (เล่นรอบ) — เน้นจังหวะ"]) 
 
with tab1: 
    core_ranking = generate_ranking_data(core["stock"].tolist(), mode="core") 
    st.dataframe(core_ranking.head(5), use_container_width=True, hide_index=True) 
    st.caption("เกณฑ์: RSI<30, ราคาต่ำกว่า EMA200, P/E, P/B, Yield") 
 
with tab2: 
    sat_ranking = generate_ranking_data(satellite["stock"].tolist(), mode="satellite") 
    st.dataframe(sat_ranking.head(5), use_container_width=True, hide_index=True) 
    st.caption("เกณฑ์: RSI<30, Stoch<20, MACD ตัดขึ้น, Fibonacci") 
 
st.markdown("---") 
st.caption("พัฒนาโดย Suchat50 — หมายเหตุ: ข้อมูลเป็นตัวอย่าง ระบบจริงจะดึงจาก API") 
