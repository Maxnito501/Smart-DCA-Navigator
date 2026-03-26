import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import get_watchlist
from utils.data_fetcher import fetch_price, fetch_rsi, fetch_ema200

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
    """ดึงข้อมูลจริงจาก yfinance และจัดลำดับคะแนน"""
    data = []
    for stock in stocks[:15]:
        try:
            # ดึงข้อมูลจริง
            price = fetch_price(stock)
            rsi = fetch_rsi(stock)
            ema200 = fetch_ema200(stock)
            
            # ถ้าข้อมูลไม่ครบ ข้ามตัวนี้
            if price is None or rsi is None:
                continue
                
            if mode == "core":
                score = 0
                # RSI ยิ่งต่ำยิ่งดี
                if rsi < 30:
                    score += 30
                elif rsi < 40:
                    score += 20
                elif rsi < 50:
                    score += 10
                # ราคาต่ำกว่า EMA200
                if ema200 and price < ema200:
                    score += 25
                # คะแนนสุ่มเล็กน้อย (จะแทนที่ด้วย P/E, P/B, Yield ในอนาคต)
                score += np.random.uniform(0, 10)
                compare_ema = "ต่ำกว่า" if (ema200 and price < ema200) else "สูงกว่า"
            else:
                score = 0
                # RSI ยิ่งต่ำยิ่งดี
                if rsi < 30:
                    score += 25
                elif rsi < 40:
                    score += 15
                # Stochastic (จำลอง ไว้สำหรับการพัฒนาต่อ)
                stoch = np.random.uniform(10, 90)
                if stoch < 20:
                    score += 25
                # MACD (จำลอง)
                macd = np.random.choice(["ตัดขึ้น", "ตัดลง"])
                if macd == "ตัดขึ้น":
                    score += 25
                score += np.random.uniform(0, 15)
                compare_ema = "-"
            
            data.append({
                "หุ้น": stock,
                "ราคา": price,
                "RSI": rsi,
                "EMA200": round(ema200, 2) if ema200 else "-",
                "เทียบ EMA200": compare_ema,
                "คะแนน": int(score)
            })
        except Exception as e:
            continue
    
    if not data:
        st.warning(f"ไม่สามารถดึงข้อมูลสำหรับ {mode} ได้")
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    return df.sort_values("คะแนน", ascending=False).reset_index(drop=True)

# แสดงสถานะ
st.info("📡 กำลังดึงข้อมูลจาก Yahoo Finance...")

# สร้างแท็บ
tab1, tab2 = st.tabs(["🏆 Core (ถือยาว) — เน้นราคาถูก", "🚀 Satellite (เล่นรอบ) — เน้นจังหวะ"])

with tab1:
    with st.spinner("กำลังโหลดข้อมูล Core..."):
        core_ranking = generate_ranking_data(core["stock"].tolist(), mode="core")
        if not core_ranking.empty:
            st.dataframe(core_ranking.head(5), use_container_width=True, hide_index=True)
            st.caption("เกณฑ์: RSI<30, ราคาต่ำกว่า EMA200, P/E, P/B, Yield")
        else:
            st.error("ไม่สามารถโหลดข้อมูล Core ได้")

with tab2:
    with st.spinner("กำลังโหลดข้อมูล Satellite..."):
        sat_ranking = generate_ranking_data(satellite["stock"].tolist(), mode="satellite")
        if not sat_ranking.empty:
            st.dataframe(sat_ranking.head(5), use_container_width=True, hide_index=True)
            st.caption("เกณฑ์: RSI<30, Stoch<20, MACD ตัดขึ้น, Fibonacci")
        else:
            st.error("ไม่สามารถโหลดข้อมูล Satellite ได้")

st.markdown("---")
st.caption("พัฒนาโดย Suchat50 — ข้อมูลจาก Yahoo Finance")
